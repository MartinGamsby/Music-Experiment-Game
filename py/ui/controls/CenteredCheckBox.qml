import QtQuick
import QtQuick.Templates as T
import QtQuick.Controls.Material
import QtQuick.Controls.Material.impl

T.CheckBox {
    id: control

    implicitWidth: Math.max(implicitBackgroundWidth + leftInset + rightInset,
                            anotherText.implicitWidth + leftPadding + rightPadding)
    implicitHeight: Math.max(implicitBackgroundHeight + topInset + bottomInset,
                             anotherText.implicitHeight + topPadding + bottomPadding,
                             anotherText.implicitHeight + implicitIndicatorHeight + topPadding + bottomPadding,
                             )

    spacing: 8
    padding: 8
    verticalPadding: padding + 7
    clip: true

    indicator: CheckIndicator {
        anchors.horizontalCenter: anotherText.horizontalCenter
        y: control.topPadding
        control: control

        Ripple {
            x: (parent.width - width) / 2
            y: (parent.height - height) / 2
            width: 28; height: 28

            z: -1
            anchor: control
            pressed: control.pressed
            active: enabled && (control.down || control.visualFocus || control.hovered)
            color: control.checked ? control.Material.highlightedRippleColor : control.Material.rippleColor
        }
    }

    contentItem: Text {
        leftPadding: control.indicator && !control.mirrored ? control.indicator.width + control.spacing : 0
        rightPadding: control.indicator && control.mirrored ? control.indicator.width + control.spacing : 0

        text: ""
        font: control.font
        color: control.enabled ? control.Material.foreground : control.Material.hintTextColor
        elide: Text.ElideRight
    }
    
    Text {
        x: control.text ? (control.mirrored ? control.width - width - control.rightPadding : control.leftPadding) : control.leftPadding + (control.availableWidth - width) / 2
        id: anotherText
        text: control.text
        y: control.topPadding + 28 // 28 == ripple height
        color: control.enabled ? control.Material.foreground : control.Material.hintTextColor
        horizontalAlignment: Text.AlignHCenter
    }
}
