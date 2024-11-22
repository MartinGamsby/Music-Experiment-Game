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
        anchors.horizontalCenter: parent.horizontalCenter
        font.pixelSize: 24
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
        
        TitleButton {
            id: newGameButton
            text: tr("NEW_GAME")
            font.pixelSize: 42
            onClicked: {
                backend.newGame()
            }
            PulsingAnimation {
                running: mainMenu.visible
                target: newGameButton
                from: 1.0
                to: 1.03
                time: 1500
            }
        }
        TitleAnchored {
            text: " "
        }
        TitleButton {
            text: tr("PLAY_MIDIS")
            onClicked: {
                backend.playMidis()
            }
        }
        TitleButton {
            text: tr("SETTINGS")
            onClicked: {
                backend.toSettings()
            }
        }
        TitleAnchored {
            text: " "
        }
        TitleButton {
            text: tr("EXIT")
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
    GamesByLogo {
        z: 1
        anchors.bottom: parent.bottom
        anchors.right: parent.right
    }
}