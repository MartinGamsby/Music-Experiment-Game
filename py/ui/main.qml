import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material

import "controls"


ApplicationWindow {
    id: rootWindow
    visible: true
	title: "Music Experiment Game"
    visibility: Window.Maximized
    color: menu.backgroundColor
    
    minimumWidth: 1280
    minimumHeight: 960

    property QtObject backend
    property QtObject model    
    
    Material.theme: Material.Dark

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
        
        Rectangle {
            id: init1
        }
    }	

    Connections {
        target: splashScreen
    
        function onTimeout()
        {
            screens.switchTo(menuView)
        }
    }
}

