import QtQuick
import QtQuick.Layouts
import QtQuick.Controls.Material

StackLayout{
    id: screens

    function currentItem(){
        return this.children[this.currentIndex]
    }

    function switchTo(item){
        for(var i in this.children){
            if(this.children[i] === item) {
                this.currentIndex = i;
                return true;
            }
        }
        return false;
    }
}