import QtQuick
import Qt5Compat.GraphicalEffects
import QtQuick.Templates as T
import QtQuick.Controls

ToolTip {
    id: control
    
    font.pixelSize: 13
    
    implicitWidth: Math.min( control.contentItem.implicitWidth +
        horizontalPadding * 2, 192 )
    enter: Transition {
        // toast_enter
        NumberAnimation { property: "opacity"; from: 0.0; to: 1.0; easing.type: Easing.OutQuad; duration: 300 }
    }
    exit: Transition {
        // toast_exit
        NumberAnimation { property: "opacity"; from: 1.0; to: 0.0; easing.type: Easing.InQuad; duration: 300 }
    }
    contentItem: Label {
        text: control.text
        font: control.font
        wrapMode: Text.Wrap
        textFormat: Text.RichText        
        horizontalAlignment: Text.AlignHCenter
    }
    background: Item {
        Rectangle {
            id: bg
            anchors.fill: parent
            implicitWidth: 192
            color: "#222222"
            radius: 4
            border.width: 0 // The border gets bigger with a dropshadow for some reason
            border.color: "#111111"
        }
        DropShadow {
            anchors.fill: bg
            horizontalOffset: 0
            verticalOffset: 5
            transparentBorder: true
            radius: 10
            color: "#000000"
            source: bg
        }
    }
    y: -implicitHeight - 5
}
