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
	title: tr("GAME_TITLE")
    visibility: Window.Maximized
    color: menu.backgroundColor
    
    minimumWidth: 1280
    minimumHeight: 960

    property QtObject backend
    property QtObject model    
    
    Material.theme: Material.Dark
    Material.accent: Material.Cyan
    
    function tr(key) {
        return backend ? ( backend.tr(key) + backend.p_ ) : ""
    }

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
            titleText: tr("GAME_TITLE")
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
            Item {
                width: gameLogo.width/2                
            }
            Text {                
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                text: tr("NEW_GAME_1")
                color: "white"
                font.pointSize: 40
                
            }
            GameLogo {
            }
        }
        Item {
            id: menuView3
            anchors.margins: 9

            LayoutItemProxy {
                anchors.fill:parent                
                target: canvas
            }
            Item {
                width: gameLogo.width/2                
            }
            Text {
                anchors.fill:parent
                
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                text: tr("NEW_GAME_1")
                color: "white"
                font.pointSize: 40
                
            }
            GameLogo {
                id: gameLogo
                anchors.right: parent.right
                anchors.top: parent.top
                width: maxSizeW
                height: maxSizeH
            }
            RowLayout {
                visible: model ? model.p_ideas.p_unlocked : false
                GrowingImage {
                    source: "qrc:/idea"
                    maxSize: 40
                }
                Text {
                    z: 10
                    text: (model ? model.p_ideas.i : 0)// + " ideas"
                    color: "white"
                    font.pointSize: 24
                    x: 10
                }
            }
        }
        RowLayout {
            id: settingsView
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 9

            SettingsMenu {
                Layout.fillWidth: true
                Layout.fillHeight: true
            }
    
            GameLogo {
            }
        }
        
        Rectangle {
            id: init1
        }
    }
    // TODO: Only visible if unlocked
    //Text {
    //    z: 10
    //    id: test1
    //    text: "debug:"
    //    color: "white"
    //    x: 10
    //    y: 50
    //}
    //Text {
    //    z: 10
    //    text: model ? model.p_language.s : "language"
    //    color: "white"
    //    x: 60
    //    y: 50
    //}
    //Text {
    //    z: 10
    //    text: model ? model.p_music_beat.i : 0
    //    color: "white"
    //    x: 90
    //    y: 50
    //}
    //Text {
    //    z: 10
    //    text: model ? model.p_title.s : "title"
    //    color: "white"
    //    x: 120
    //    y: 50
    //}
    
    Connections {
        target: model
    
        function onState_updated() {
            if( model.p_state_id == StateEnum.PLAY_MIDIS ) {
                screens.switchTo(menuView)
            }
            if( model.p_state_id == StateEnum.GAME ) {
                screens.switchTo(menuView3)
            }
            if( model.p_state_id == StateEnum.MAIN_MENU ) {
                screens.switchTo(mainMenuView)
                //test1.text = model._title
            }
            if( model.p_state_id == StateEnum.SETTINGS ) {
                screens.switchTo(settingsView)
            }
        }
    }
}

