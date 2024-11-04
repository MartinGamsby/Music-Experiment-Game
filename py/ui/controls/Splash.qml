import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material

// For State and MusicState enums
import com.martingamsby.music 1.0

Item {
    id: splashRoot

    property alias titleText: title.text
    property alias statusText: statusLine1.text
    property alias statusText2: statusLine2.text
    property alias statusText3: statusLine3.text
    
    property bool finished: false

    signal timeout()

    component Title: Text {
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        anchors.horizontalCenter: parent.horizontalCenter
        color: "white"
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
        anchors.topMargin: parent.height * .3
        anchors.bottomMargin: parent.height * .3
        
    
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
    
            Image {
                id: logo
                source: "qrc:/logo"
                width: 300
                fillMode: Image.PreserveAspectFit
                anchors.horizontalCenter: parent.horizontalCenter
                            
                SequentialAnimation {
                    running: true
                    ScaleAnimator {
                        duration: 800; target: logo
                        from: 0.8; to: 1.2
                        easing.type: Easing.OutBack;//Elastic;
                    }
                    ScaleAnimator {
                        duration: 1500; target: logo
                        from: 1.2; to: 1.0
                        easing.type: Easing.InQuad;                 
                    }
                }
            }
    
            Title {
                id: title
                font.pixelSize: 64
                text: "Music Experiment Game"
            }
    
            Title {
                id: statusLine0
                font.pixelSize: 32
                text: "Loading, please wait"
            }
    
            Title {
                id: statusLine1
                font.pixelSize: 32
                text: " "
            }
            
            Title {
                id: statusLine2
                font.pixelSize: 32
                text: " "
            }
            Title {
                id: statusLine3
                font.pixelSize: 32
                text: " "
            }
        }
    }
    
    Timer {
        id: splashTimer
        interval: 1000 // Show splash screen for at least this duration
        repeat: false
        running: false
    
        onTriggered: {
            splashRoot.finished = true
            splashRoot.timeout()
        }
    }
    
    Connections {
        target: model
    
        function onState_updated() {
            if( model.p_state_id == StateEnum.WELCOME ) {
                splashTimer.start()
            }
        }
    }
}