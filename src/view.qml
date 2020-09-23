import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls.Material 2.15

ApplicationWindow {
    Material.theme: Material.Light
    Material.primary: Material.Teal
    Material.accent: Material.Red
    title: Consts.MainTitle
    visible: true
    height: 1280
    width: 1024

    RowLayout {
        anchors.fill: parent
        spacing: 6

        Page {
            Layout.preferredWidth: parent.width * 0.3
            Layout.fillHeight: true
            header: Pane {
                Material.background: Material.primary
                Material.elevation: 6
                width: parent.width
                height: parent.height * 0.07

                Label {
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.leftMargin: 8
                    text: Consts.ImageListTitle
                    font.pixelSize: 18
                    color: "white"
                }

                RoundButton {
                    anchors.right: parent.right
                    anchors.verticalCenter: parent.verticalCenter
                    flat: true
                    display: AbstractButton.IconOnly
                    icon.color: "white"
                    icon.source: "../res/add_image.png"
                }
            }
        }

        Page {
            Layout.fillWidth: true
            Layout.fillHeight: true
            header: Pane {
                Material.background: Material.primary
                Material.elevation: 6
                width: parent.width
                height: parent.height * 0.07

                Label {
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: Consts.ArtTitle
                    font.pixelSize: 18
                    color: "white"
                }

                RoundButton {
                    id: pauseAnimationButton
                    anchors.right: parent.right
                    anchors.verticalCenter: parent.verticalCenter
                    flat: true
                    display: AbstractButton.IconOnly
                    icon.color: "white"
                    icon.source: "../res/pause.png"
                }

                RoundButton {
                    id: playAnimationButton
                    anchors.right: pauseAnimationButton.left
                    anchors.verticalCenter: parent.verticalCenter
                    flat: true
                    display: AbstractButton.IconOnly
                    icon.color: "white"
                    icon.source: "../res/play.png"
                }
            }
        }
    }
}