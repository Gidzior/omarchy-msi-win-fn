import QtQuick
import Quickshell
import Quickshell.Io
import qs.Ui

Item {
  id: root
  property var bar
  property string moduleName
  property var settings
  property string label: "󰌌 ?"
  property string description: "Reading Win/Fn state…"
  readonly property string physicalFnSide: settings && settings.physicalFnSide === "right" ? "right" : "left"

  implicitWidth: button.implicitWidth
  implicitHeight: button.implicitHeight

  Process {
    id: toggle
    command: ["sudo", "-n", "/usr/local/sbin/omarchy-toggle-win-fn"]
    onExited: function(exitCode, exitStatus) {
      if (!status.running) status.running = true
      if (exitCode !== 0)
        Quickshell.execDetached(["notify-send", "Win/Fn", "Could not switch keys. Check the helper installation and MSI driver."])
    }
  }

  Process {
    id: status
    command: ["cat", "/sys/devices/platform/msi-ec/win_key"]
    stdout: StdioCollector {
      waitForEnd: true
      onStreamFinished: {
        try {
          const side = text.trim()
          if (side !== "left" && side !== "right") throw new Error("Unknown state")
          const key = side === root.physicalFnSide ? "FN" : "WIN"
          root.label = "󰌌 " + key
          root.description = "Super: " + key + " (" + side + ")"
        } catch (error) {
          root.label = "󰌌 ?"
          root.description = "MSI Win/Fn state unavailable"
        }
      }
    }
  }

  Timer {
    interval: 3000
    running: true
    repeat: true
    triggeredOnStart: true
    onTriggered: if (!status.running) status.running = true
  }

  WidgetButton {
    id: button
    anchors.fill: parent
    bar: root.bar
    text: root.label
    tooltipText: root.description
    horizontalMargin: 7
    fontSize: 12
    onPressed: function(mouseButton) {
      if (mouseButton === Qt.LeftButton && !toggle.running) toggle.running = true
    }
  }
}
