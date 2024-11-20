import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material

// For State and MusicState enums
import com.martingamsby.music 1.0

Item {
    id: mainMenu

    component Title: Text {
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        anchors.horizontalCenter: parent.horizontalCenter
        font.pixelSize: 32
        color: "white"
    }
    component TitleButton: Button {
        anchors.horizontalCenter: parent.horizontalCenter
        font.pixelSize: 32
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
                            
                SequentialAnimation {
                    running: mainMenu.visible
                    ScaleAnimator {
                        duration: 250; target: logo
                        from: 13.0; to: 1.1
                        easing.type: Easing.InQuad;//Elastic;
                    }
                    SequentialAnimation {
                        loops: -1
                        ScaleAnimator {
                            duration: 500; target: logo
                            from: 1.13; to: 1.0
                            easing.type: Easing.InQuad;                 
                        }
                        ScaleAnimator {
                            duration: 500; target: logo
                            from: 1.0; to: 1.13
                            easing.type: Easing.InQuad;                 
                        }
                    }
                }
            }    
            Title {
                id: title
                font.pixelSize: 64
                text: tr("GAME_TITLE")
            }
            Title {
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
            text: tr("NEW_GAME")
            onClicked: {
                backend.newGame()
            }
        }
        Title {
            text: "~"
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
        Title {
            text: "~"
            visible: false
        }
        
    }
    FlagButtons {
    }
    GamesByLogo {
        z: 1
        anchors.bottom: parent.bottom
        anchors.right: parent.right
    }
}