import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material

import "controls"
import "pages"

// For State and MusicState enums
import com.martingamsby.music 1.0

ApplicationWindow {
    id: rootWindow
    visible: true
	title: tr("GAME_TITLE")
    visibility: model ? (model.p_fullscreen.b ? Window.FullScreen : Window.Maximized) : Window.FullScreen
    color:  "#222222"//menu.backgroundColor
    
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
        
    MusicCanvas {
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
        
        // TODO: To "page" qml file.
        PlayMidis {
            id: menuView

            LayoutItemProxy {
                target: canvas
                z: -1
                anchors.fill: parent
                //anchors.right: menuView.menu.left
                //Layout.fillWidth: true
                //Layout.fillHeight: true
            }
        }
        Game {
            id: menuView3
            LayoutItemProxy {
                anchors.fill:parent
                target: canvas
                z: -1
            }
        }
        RowLayout {
            id: settingsView
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 9

            ColumnLayout {
                SettingsMenu {
                    Layout.fillWidth: true
                }                
                FlagButtons {
                    Layout.margins: 9
                }
            }
            ColumnLayout {
                Stats {
                    Layout.fillWidth: true
                }    
                GameLogo {
                }
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

