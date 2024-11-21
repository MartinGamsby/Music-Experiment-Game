import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material


Item {
    id: imageContainer
    property bool isHovered: false
    property int maxSize: 100
    property int size: isHovered ? maxSize : maxSize*0.9
    
    Layout.maximumWidth: maxSize
    Layout.maximumHeight: maxSize
    Layout.minimumWidth: maxSize
    Layout.minimumHeight: maxSize
    Layout.alignment: Qt.AlignRight | Qt.AlignBottom
    
    
    property alias source: image.source
  
    function onClicked() {}
        
    Image {
        id: image
        
        anchors.centerIn: parent
        
        width: size
        height: size
        source: "qrc:/logo"
        fillMode: Image.PreserveAspectFit
        mipmap: true
        smooth: true
        
        MouseArea {
            id: mouseArea
            anchors.fill: parent        
            hoverEnabled: true
            onClicked: {
                imageContainer.onClicked()
            }
            onEntered: {
                isHovered = true
            }
            onExited: {
                isHovered = false
            }
        }
    }
    Behavior on size { 
        PropertyAnimation { easing.type: Easing.InOutQuad } 
    }
}