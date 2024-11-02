import QtQuick
import QtQuick.Layouts
import QtQuick.Controls.Basic
import QtQuick.Controls.Material

Item {
    id: menuRoot
    implicitWidth: buttons.width
    implicitHeight: buttons.height
    readonly property color backgroundColor: "#222222"
    
    Button {
        id: buttons
        text: "test"
        onClicked: {
            backend.ok_pressed(buttons.text)
        }
    }
}
