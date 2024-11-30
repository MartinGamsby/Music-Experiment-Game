import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material

// For State and MusicState enums
import com.martingamsby.music 1.0

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
        id: musicDescription
        visible: model ? (model.p_music_description.p_unlocked) : false
        font.pixelSize: 20
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: playbackState.left
        anchors.margins: 9
        anchors.bottomMargin: 19
        
        wrapMode: Text.Wrap
        textFormat: Text.RichText      
    
        text: model ? model.p_music_description.s : ""
        horizontalAlignment: Text.AlignLeft
    }
    
    // TODO: Move to another file?
    Title {
        id: playbackState
        visible: model ? (model.p_state_id != StateEnum.GAME || (model.p_gui_playback.p_unlocked && model.p_gui_playback.b)) : false
        font.pixelSize: 20
        anchors.bottom: parent.bottom
        anchors.right: parent.right
        anchors.margins: 9
        anchors.bottomMargin: 19
    
        text: model ? model.p_music_state_pretty_name : ""        
    }
    Rectangle {
        visible: playbackState.visible
        color: enabled ? Material.foreground : Material.hintTextColor
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.margins: 0
        height: 10
        width: model ? (model.p_music_progress.f * parent.width) : 0
    }
}
