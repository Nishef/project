import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.12

Window {
    id: loginwindow
    width: 640
    height: 480
    visible: true
    color: "#ffffff"
    title: qsTr("Hello World")

    TextField {
        id: textField
        x: 177
        y: 148
        placeholderText: qsTr("Text Field")
    }

    TextField {
        id: textField1
        x: 177
        y: 205
        placeholderText: qsTr("Text Field")
    }
}
