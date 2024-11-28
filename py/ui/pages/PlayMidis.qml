import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material

import "../controls"

// For State and MusicState enums
import com.martingamsby.music 1.0

Item {
    default property alias content: contentItem.children
    
    Item {
        id: contentItem
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.right: menu.left
        anchors.rightMargin: 9
    }
    Menu {
        id: menu
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
    }
}