import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material

Rectangle {
    color: "black"
    
    Ripple {
        anchors.fill: parent
        rippling: model ? (!((model.p_music_beat.i - 1) % 4)) : 0
    }    
    
    TitleAnchored {            
        anchors.centerIn: parent
        text: model ? model.p_title.s : ""
        font.pixelSize: 60
    }
    Title {
        font.pixelSize: 20
        anchors.bottom: parent.bottom
        anchors.right: parent.right
        anchors.margins: 9
        anchors.bottomMargin: 19
    
        text: model ? model.p_music_state_pretty_name : ""        
    }
    Rectangle {
        color: enabled ? Material.foreground : Material.hintTextColor
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.margins: 0
        height: 10
        width: model ? (model.p_music_progress.f * parent.width) : 0
    }
}
