import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material

import "controls"

// For State and MusicState enums
import com.martingamsby.music 1.0

ApplicationWindow {
    id: rootWindow
    visible: true
	title: qsTr("Music Experiment Game")
    visibility: Window.Maximized
    color: menu.backgroundColor
    
    minimumWidth: 1280
    minimumHeight: 960

    property QtObject backend
    property QtObject model    
    
    Material.theme: Material.Dark
    Material.accent: Material.Cyan

    NumberAnimation on opacity {
        from: 0
        to: 1
        duration: 500//1000
        running: true
    }
        
    Menu {
        id: menu
    }

    Canvas {
        id: canvas
        Layout.fillWidth: true
        Layout.fillHeight: true
    }

    Multiscreen {
        id: screens
        anchors.fill: parent

        Splash {
            id: splashScreen
            titleText: "Music Experiment Game"
            statusText: model ? model.p_state_pretty_name : "..."
            
            onTimeout: {
                backend.toMainMenu(false)
            }
        }

        MainMenu {
            id: mainMenuView
        }
        
        RowLayout {
            id: menuView
            spacing: 9
            anchors.margins: 9

            LayoutItemProxy {
                target: canvas
            }

            LayoutItemProxy {
                target: menu
                Layout.fillWidth: false
                Layout.fillHeight: true
            }
        }
        RowLayout {
            id: menuView2
            spacing: 9
            anchors.margins: 9

            LayoutItemProxy {
                target: canvas
            }
            Text {
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                text: "That's it!\nThe game is\nbeing developed\nright now,\nhopefully..."
                color: "white"
                font.pointSize: 40
            }
            GameLogo {
            }
        }
        
        Rectangle {
            id: init1
        }
    }
    
    Connections {
        target: model
    
        function onState_updated() {
            if( model.p_state_id == StateEnum.PLAY_MIDIS ) {
                screens.switchTo(menuView)
            }
            if( model.p_state_id == StateEnum.GAME ) {
                screens.switchTo(menuView2)
            }
            if( model.p_state_id == StateEnum.MAIN_MENU ) {
                screens.switchTo(mainMenuView)
            }
        }
    }
}

