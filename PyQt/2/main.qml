import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15




Window {
    id: window
    width: 500
    height: 476
    visible: true
    title: qsTr("سلام")
    flags: Qt.WindowCloseButtonHint|Qt.WindowMinimizeButtonHint|Qt.CustomizeWindowHint|Qt.Dialog|Qt.WindowTitleHint

    RoundButton {
        id: roundButton
        x: 155
        y: 413
        width: 189
        height: 53
        text: "hello"
        anchors.horizontalCenter: parent.horizontalCenter
        font.strikeout: false
        focusPolicy: Qt.StrongFocus
        font.underline: false
        font.italic: false
        font.family: "Courier"
        font.preferShaping: true
        highlighted: true
        font.bold: false
        wheelEnabled: false
        spacing: 0
        font.pointSize: 9
    }

    Button {
        id: button
        x: 190
        y: 329
        width: 121
        height: 50
        text: qsTr("Button")
        anchors.horizontalCenter: parent.horizontalCenter
        layer.format: ShaderEffectSource.RGBA
        font.wordSpacing: 0
        baselineOffset: 104
        font.family: "Arial"
        highlighted: false
        Material.background: "darkgrey"
        font.bold: false
        spacing: 0
    }

    Label {
        id: label
        x: 350
        y: 165
        width: 62
        height: 20
        color: "#000000"
        text: qsTr("نام کاربری:")
        anchors.left: roundButton.right
        anchors.leftMargin: 37
        font.family: "Arial"
        textFormat: Text.PlainText
        font.pointSize: 12
    }

    Label {
        id: label1
        x: 350
        y: 245
        width: 62
        height: 19
        color: "#000000"
        text: qsTr("پسورد:")
        anchors.left: label.left
        anchors.right: label.right
        anchors.leftMargin: 0
        font.family: "Arial"
        font.pointSize: 11
    }

    TextField {
        id: lineEditusername
        x: 127
        y: 155
        width: 180
        height: 50
        color: "#000000"
        font.family: "Arial"
        placeholderTextColor: "#7f000000"
        placeholderText: "نام کاربری"
        font.pointSize: 14
        selectByMouse: true
    }

    TextField {
        id: textFieldpassword
        x: 127
        y: 230
        width: 180
        height: 50
        anchors.verticalCenter: label1.verticalCenter
        echoMode: "Password"
        font.family: "Arial"
        placeholderTextColor: "#7f000000"
        antialiasing: true
        placeholderText: "کلمه عبور"
        activeFocusOnTab: true
        font.pointSize: 14
        selectByMouse: true
    }

    Rectangle {
        id: rectangle
        x: 127
        y: 155
        width: 180
        height: 45
        color: "#aca4a4"
    }
    

//    Material.theme: Material.Yellow

}



/*##^##
Designer {
    D{i:0;formeditorColor:"#ffffff"}
}
##^##*/
