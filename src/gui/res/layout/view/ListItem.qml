import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls.Material 2.15

Pane {
    objectName: "artListItem"
    width: parent.width
    height: Consts.ArtListItemHeight
    Material.elevation: Consts.ArtListItemElevation
    padding: 0

    Image {
        id: artListItemImg
        width: parent.width
        height: Consts.ArtListItemImageHeight
        fillMode: Image.PreserveAspectCrop
        source: "../../drawable/test2.jpg"  // TODO
    }
    ItemDelegate {
        anchors.fill: parent
        onClicked: {
            drawer.close()
        }
    }
    RowLayout {
        anchors.top: artListItemImg.bottom
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.leftMargin: 16

        Label {
            Layout.fillWidth: parent
            Layout.fillHeight: parent
            verticalAlignment: Text.AlignVCenter
            text: name  // TODO
            elide: Text.ElideRight
            font.pixelSize: Consts.ArtListItemFontSize
        }
        RoundButton {
            Layout.fillHeight: parent
            flat: true
            icon.source: Consts.ArtListInfoImgSrc
            onClicked: listItemMenu.open()

            Menu {
                id: listItemMenu
                y: parent.height
                topPadding: 0
                bottomPadding: topPadding

                Action {
                    text: Consts.ArtListItemPropertiesBtn
                    onTriggered: { drawer.close() }
                }
                Action {
                    text: Consts.ArtListItemRemoveBtn
                    onTriggered: {
                        ArtModels.delete_person(index)
                    }
                }
            }
        }
    }
}