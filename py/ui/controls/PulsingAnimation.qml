import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material

SequentialAnimation {
    id: anim
    required property Item target
    property real from: 1.13
    property real to: 1.0
    property int scaleDownTime: 250
    property int time: 500
    
    ScaleAnimator {
        duration: scaleDownTime; target: anim.target
        from: 13.0; to: anim.from
        easing.type: Easing.InQuad;
    }
    SequentialAnimation {
        loops: -1
        ScaleAnimator {
            duration: anim.time; target: anim.target
            from: anim.from; to: anim.to
            easing.type: Easing.InQuad;                 
        }
        ScaleAnimator {
            duration: anim.time; target: anim.target
            from: anim.to; to: anim.from
            easing.type: Easing.InQuad;                 
        }
    }
}