import QtQuick
import QtQuick.Templates as T
import QtQuick.Controls.impl
import QtQuick.Controls.Material
import QtQuick.Controls.Material.impl

T.Button {
    id: control
    property bool rippling: false
    
    background: Rectangle {
        color: control.Material.buttonColor(control.Material.theme, control.Material.background,
            control.Material.accent, control.enabled, control.flat, control.highlighted, control.checked)
        clip: true
        Ripple {
            id: ripple
            clipRadius: parent.radius
            width: parent.width
            height: parent.height
            pressed: control.pressed || control.rippling
            active: enabled && (control.down || control.visualFocus || control.hovered)
            color: control.flat && control.highlighted ? control.Material.highlightedRippleColor : control.Material.rippleColor
            
        }
    }
    onClicked: {
        // By default the ripple is centered, then it moves to the last click.
        ripple.anchor = control
    }
}
