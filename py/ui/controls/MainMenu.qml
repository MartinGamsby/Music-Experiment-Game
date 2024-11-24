import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material

// For State and MusicState enums
import com.martingamsby.music 1.0

Item {
    id: mainMenu

    component TitleButton: Button {
        font.pixelSize: 24
    }	
    component TitleButtonCentered: TitleButton {
        anchors.horizontalCenter: parent.horizontalCenter
    }	
	
    Image {
        id: image
        anchors.fill: parent
        source: "qrc:/bg"
        fillMode: Image.PreserveAspectCrop
    }

    Item {
        anchors.fill: parent
        anchors.centerIn: parent
    
        anchors.leftMargin: 0
        anchors.rightMargin: 0
        anchors.topMargin: parent.height * .2
        anchors.bottomMargin: parent.height * .4
        z: 3
    
        Rectangle {
            anchors.fill: parent
            opacity: .5
            color: "#222222"
        }
    
        Column {
            anchors.centerIn: parent
            anchors.leftMargin: 100
            anchors.rightMargin: 100
            anchors.topMargin: 100
            anchors.bottomMargin: 100
            z: 4
    
            Image {
                id: logo
                source: "qrc:/logo"
                width: 300
                sourceSize.width: width*10
                fillMode: Image.PreserveAspectFit
                anchors.horizontalCenter: parent.horizontalCenter
                mipmap: true
                smooth: true
                z: 5 // over everything
                
                PulsingAnimation {
                    running: mainMenu.visible && (model ? (model.p_music_state_id == MusicStateEnum.PLAYING) : false)
                    target: logo
                }
            }    
            TitleAnchored {
                id: title
                font.pixelSize: 64
                text: tr("GAME_TITLE")
            }
            TitleAnchored {
                id: statusLine0
                text: " "
            }
            
        }
    }
        
    Column {
        z: 2
        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottomMargin: 50
    
        PulsingAnimation {
            running: mainMenu.visible
            target: loadGameButton.visible ? loadGameButton : newGameButton
            from: 1.0
            to: 1.03
            time: 1500
            scaleDownTime: 0
        }
        
        TitleButtonCentered {
            id: loadGameButton
            visible: backend ? backend.p_has_save_files.b : false
            text: tr("LOAD_GAME")
            font.pixelSize: 42
            onClicked: {
                backend.loadGame()
            }
        }
        TitleButton {
            id: newGameButton
            
            anchors.right: loadGameButton.right
            
            text: tr("NEW_GAME")
            font.pixelSize: loadGameButton.visible ? 14 : 42
            onClicked: {
                backend.newGame()
            }
        }
        TitleButtonCentered {
            text: tr("PLAY_MIDIS")
            anchors.left: loadGameButton.left
            onClicked: {
                backend.playMidis()
            }
        }
        TitleButtonCentered {
            text: tr("SETTINGS")
            anchors.left: loadGameButton.left
            onClicked: {
                backend.toSettings()
            }
        }
        TitleButtonCentered {
            text: tr("EXIT")
            anchors.right: loadGameButton.right
            font.pixelSize: 16
            onClicked: {
                backend.exit()
            }
        }
        
    }
    FlagButtons {
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.margins: 9
    }
    GamesByLogoAnimated {
        z: 1
        anchors.bottom: parent.bottom
        anchors.right: parent.right
    }
}