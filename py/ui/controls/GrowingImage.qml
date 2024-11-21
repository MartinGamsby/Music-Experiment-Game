import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material


Item {
    id: imageContainer
    property bool isHovered: false
    property int maxSize: 100
    property int maxSizeW: maxSize
    property int maxSizeH: maxSize
    property int sizeW: isHovered ? maxSizeW : maxSizeW*shrinkFactor
    property int sizeH: isHovered ? maxSizeH : maxSizeH*shrinkFactor
    property real shrinkFactor: 0.9
    
    Layout.minimumWidth: maxSizeW
    Layout.maximumWidth: maxSizeW
    Layout.minimumHeight: maxSizeH
    Layout.maximumHeight: maxSizeH
    Layout.alignment: Qt.AlignRight | Qt.AlignBottom
    
    
    property alias source: image.source
    property alias fillMode: image.fillMode    
  
    function onClicked() {}
        
    Image {
        id: image
        
        anchors.centerIn: parent
        
        width: sizeW
        height: sizeH
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
    Behavior on sizeW { 
        PropertyAnimation { easing.type: Easing.InOutQuad } 
    }
    Behavior on sizeH { 
        PropertyAnimation { easing.type: Easing.InOutQuad } 
    }
}