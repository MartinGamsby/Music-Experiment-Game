import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material
import QtMultimedia

// For State and MusicState enums
import com.martingamsby.music 1.0

Rectangle {
    color: "black"
    
    Ripple {
        anchors.fill: parent
        rippling: model ? (!model.p_is_video.b && !((model.p_music_beat.i - 1) % 4)) : 0
    }    
    
    TitleAnchored {            
        anchors.centerIn: parent
        text: model ? model.p_title.s : ""
        font.pixelSize: 60
    }
    
    // TODO: Move to another file?
    Title {
        id: playbackState
        visible: model ? (model.p_state_id != StateEnum.GAME || (model.p_gui_playback.p_unlocked && model.p_gui_playback.b)) : false
        font.pixelSize: 20
        anchors.bottom: mediaPlayerBox.top
        anchors.horizontalCenter: parent. horizontalCenter
        anchors.margins: 9
        anchors.bottomMargin: 19
    
        text: model ? model.p_music_state_pretty_name : ""        
    }
    Rectangle {
        id: mediaPlayerBox
        width: parent.width - 18
        height: visible ? parent.height*0.45 : 0
        anchors.bottom: playbackBar.top
        anchors.horizontalCenter: parent. horizontalCenter
        
        radius: 9
        color:"black"
        visible: model ? (model.p_music_state_id == MusicStateEnum.PLAYING && model.p_is_video.b) : false

        MediaPlayer {
            id: mediaPlayer
            objectName: "mediaPlayer"
            
            
            videoOutput: vidOut
            audioOutput: AudioOutput {
                volume: 1.0
            }
            source: model ? model.p_gui_play_video.s : ""
            autoPlay: false
            onPositionChanged: {
                if( mediaPlayer.duration > 0 )
                {
                    model.music_cb(mediaPlayer.position, mediaPlayer.duration, true)
                }
            }
            
        }
        Connections{
            target: model ? model.p_gui_play_video : null
            function onValue_updated(){
                if( model.p_is_video.b ) {
                    mediaPlayer.play() // autoPlay instead? (Choppy sometimes?)
                }
                else
                {
                    mediaPlayer.stop()
                }                   
            }
        }
        
        ColumnLayout {
            anchors.fill: parent
            VideoOutput {
                id: vidOut
                Layout.fillWidth: true
                // Exact multiplier to be a (possibly) sharper rescale
                Layout.minimumHeight: 192*2
            }
            Rectangle {
                id: videoPlayer
                width: parent.width
                height: 50
                color: "black"
                Layout.margins: 9
                Layout.fillWidth: true

                RowLayout {
                    anchors.left: parent.left
                    anchors.right: parent.right
                    
                    spacing: 10

                    Button {
                        text: mediaPlayer.playbackState === MediaPlayer.PlayingState ? tr("PAUSE") : tr("PLAY")
                        onClicked: {
                            if (mediaPlayer.playbackState === MediaPlayer.PlayingState) {
                                mediaPlayer.pause();
                            } else {
                                mediaPlayer.play();
                            }
                        }
                    }

                    Slider {
                        id: progressSlider
                        
                        Layout.fillWidth: true
                        
                        value: mediaPlayer.position
                        to: mediaPlayer.duration
                        onValueChanged: {
                            if (progressSlider.pressed) {
                                mediaPlayer.position = progressSlider.value;
                            }
                        }
                    }
                }
            }
        }
    }
    Rectangle {
        id: playbackBar
        visible: playbackState.visible && !mediaPlayerBox.visible
        color: enabled ? Material.foreground : Material.hintTextColor
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.margins: 0
        height: visible ? 10 : 0
        width: model ? (model.p_music_progress.f * parent.width) : 0
    }
}
