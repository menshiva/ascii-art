import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Dialog {
    property int itemIndex: -1
    width: parent.width * Consts.DialogWidthCoefficient
    anchors.centerIn: Overlay.overlay
    title: Consts.AddImgButtonText
    modal: true
    closePolicy: Popup.NoAutoClose
    Overlay.modal: Rectangle { color: Consts.ShadowColor }

    ColumnLayout {
        anchors.fill: parent
        spacing: Consts.DialogItemSpacing

        Frame {
            Layout.fillWidth: true

            TextField {
                id: addImageDialogNameBox
                width: parent.width
                placeholderText: Consts.AddImageDialogNameTitle
                selectByMouse: true
                onTextChanged: {
                    addImageBtn.enabled = addImageDialogNameBox.text != "" && addImageDialogPathBox.text != ""
                }
            }
        }
        Frame {
            Layout.fillWidth: true

            RowLayout {
                anchors.fill: parent

                TextField {
                    id: addImageDialogPathBox
                    objectName: "addImageDialogPathBox"
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Layout.leftMargin: Consts.AddImageDialogPathBoxLeftMargin
                    Layout.rightMargin: Consts.AddImageDialogPathBoxRightMargin
                    placeholderText: Consts.AddImageDialogImgPathTitle
                    readOnly: true
                    onTextChanged: {
                        addImageBtn.enabled = addImageDialogNameBox.text != "" && addImageDialogPathBox.text != ""
                    }
                }
                Button {
                    objectName: "addImageDialogBrowseBtn"
                    text: Consts.AddImageDialogBrowseBtn
                    highlighted: true
                    enabled: itemIndex == -1
                }
            }
        }
    }
    footer: DialogButtonBox {
        Button {
            id: addImageBtn
            enabled: false
            flat: true
            text: itemIndex == -1 ? Consts.AddImageDialogAddBtn : Consts.AddImageDialogSaveBtn
            DialogButtonBox.buttonRole: DialogButtonBox.DestructiveRole
            onClicked: {
                if (itemIndex == -1) {
                    ArtModels.add_art(addImageDialogNameBox.text, addImageDialogPathBox.text)
                    addImageDialogNameBox.text = ""
                    addImageDialogPathBox.text = ""
                }
                else {
                    ArtModels.edit_art(itemIndex, addImageDialogNameBox.text, addImageDialogPathBox.text)
                    addImageDialog.close()
                }
            }
        }
        Button {
            flat: true
            text: Consts.DialogCancelButtonText
            DialogButtonBox.buttonRole: DialogButtonBox.AcceptRole
        }
    }

    function openDialog(index, name, path) {
        itemIndex = index
        addImageDialogNameBox.text = name
        addImageDialogPathBox.text = path
        open()
    }
}