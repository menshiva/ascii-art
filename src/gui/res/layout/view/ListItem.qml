import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls.Material 2.15

Item {
    required property int index
    required property string name
    required property string path
    required property bool contrast
    required property bool negative
    required property bool convolution
    id: artListItem
    width: ListView.view.width
    height: Consts.ArtListItemHeight

    Pane {
        anchors.fill: parent
        anchors.leftMargin: Consts.ArtListItemMargin
        anchors.rightMargin: anchors.leftMargin
        Material.elevation: Consts.ArtListItemElevation
        padding: 0

        Image {
            id: artListItemImg
            width: parent.width
            height: Consts.ArtListItemImageHeight
            fillMode: Image.PreserveAspectCrop
            source: path
        }
        ItemDelegate {
            anchors.fill: parent
            highlighted: artListItem.ListView.isCurrentItem
            onClicked: {
                artList.currentIndex = index
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
                text: name
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
                        onTriggered: addImageDialog.openDialog(
                            index, name, path, contrast, negative, convolution
                        )
                    }
                    Action {
                        text: Consts.ArtListItemRemoveBtn
                        onTriggered: ArtFactory.remove_art(index)
                    }
                }
            }
        }
    }
}