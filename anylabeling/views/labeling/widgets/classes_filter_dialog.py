from typing import List, Optional

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
)

from anylabeling.views.labeling.utils.style import (
    get_cancel_btn_style,
    get_dialog_style,
    get_ok_btn_style,
)
from anylabeling.views.labeling.utils.theme import get_theme
from anylabeling.views.labeling.widgets.searchable_model_dropdown import (
    SearchBar,
)


def _list_widget_style() -> str:
    t = get_theme()
    return f"""
        QListWidget {{
            background-color: {t["background_secondary"]};
            color: {t["text"]};
            border: 1px solid {t["border"]};
            border-radius: 6px;
            outline: none;
            selection-background-color: {t["selection"]};
            selection-color: {t["selection_text"]};
        }}
        QListWidget::item {{
            padding: 4px 8px;
            min-height: 28px;
        }}
        QListWidget::item:selected {{
            background-color: {t["selection"]};
            color: {t["selection_text"]};
        }}
        QListWidget::item:hover {{
            background-color: {t["surface_hover"]};
        }}
        QListWidget::indicator {{
            width: 14px;
            height: 14px;
            border-radius: 3px;
            border: 1px solid {t["border_light"]};
            background-color: {t["background"]};
            margin-right: 4px;
        }}
        QListWidget::indicator:checked {{
            background-color: {t["primary"]};
            border-color: {t["primary"]};
            image: url(:/images/images/checkmark-white.svg);
        }}
    """


class ClassesFilterDialog(QDialog):
    """Dialog for selecting a subset of classes to filter model predictions."""

    def __init__(
        self,
        classes: List[str],
        filter_classes: Optional[List[str]] = None,
        parent=None,
    ) -> None:
        """
        Args:
            classes (List[str]): All class names from the loaded model.
            filter_classes (Optional[List[str]]): Currently active class
                name filter, or None to indicate all classes are active.
            parent: Parent widget.
        """
        super().__init__(parent)
        self._classes = classes
        self.setWindowTitle(self.tr("Filter Classes"))
        self.setMinimumWidth(520)
        self.setMinimumHeight(400)
        self.setStyleSheet(get_dialog_style() + _list_widget_style())
        self._build_ui(filter_classes)

    def _build_ui(self, filter_classes: Optional[List[str]]) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        self._search_bar = SearchBar(self)
        self._search_bar.setPlaceholderText(self.tr("Search classes..."))
        self._search_bar.textChanged.connect(self._on_search)
        layout.addWidget(self._search_bar)

        self._list = QListWidget()
        self._list.setUniformItemSizes(True)
        self._list.setSelectionMode(QListWidget.SelectionMode.NoSelection)
        for cls_name in self._classes:
            item = QListWidgetItem(cls_name)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            checked = filter_classes is None or (
                cls_name in filter_classes if filter_classes else True
            )
            item.setCheckState(
                Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked
            )
            item.setSizeHint(QSize(0, 28))
            self._list.addItem(item)
        self._list.itemChanged.connect(self._on_item_changed)
        layout.addWidget(self._list)

        btn_row = QHBoxLayout()
        btn_row.setContentsMargins(0, 4, 0, 0)
        btn_row.setSpacing(8)

        self._toggle_btn = QPushButton()
        self._toggle_btn.setStyleSheet(get_cancel_btn_style())
        self._toggle_btn.clicked.connect(self._toggle_all)
        btn_row.addWidget(self._toggle_btn)
        self._refresh_toggle_text()

        btn_row.addStretch()

        cancel_btn = QPushButton(self.tr("Cancel"))
        cancel_btn.setStyleSheet(get_cancel_btn_style())
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)

        ok_btn = QPushButton(self.tr("Confirm"))
        ok_btn.setStyleSheet(get_ok_btn_style())
        ok_btn.clicked.connect(self.accept)
        btn_row.addWidget(ok_btn)

        layout.addLayout(btn_row)

    def _on_search(self, text: str) -> None:
        text = text.strip().lower()
        for i in range(self._list.count()):
            item = self._list.item(i)
            item.setHidden(bool(text) and text not in item.text().lower())

    def _visible_all_checked(self) -> bool:
        return all(
            self._list.item(i).checkState() == Qt.CheckState.Checked
            for i in range(self._list.count())
            if not self._list.item(i).isHidden()
        )

    def _all_checked(self) -> bool:
        return all(
            self._list.item(i).checkState() == Qt.CheckState.Checked
            for i in range(self._list.count())
        )

    def _refresh_toggle_text(self) -> None:
        if self._visible_all_checked():
            self._toggle_btn.setText(self.tr("Deselect All"))
        else:
            self._toggle_btn.setText(self.tr("Select All"))

    def _on_item_changed(self, _item: QListWidgetItem) -> None:
        self._refresh_toggle_text()

    def _toggle_all(self) -> None:
        target = (
            Qt.CheckState.Unchecked
            if self._visible_all_checked()
            else Qt.CheckState.Checked
        )
        self._list.itemChanged.disconnect(self._on_item_changed)
        for i in range(self._list.count()):
            if not self._list.item(i).isHidden():
                self._list.item(i).setCheckState(target)
        self._list.itemChanged.connect(self._on_item_changed)
        self._refresh_toggle_text()

    def get_selected_classes(self) -> List[str]:
        """
        Returns:
            List[str]: Names of the checked classes.
        """
        return [
            self._list.item(i).text()
            for i in range(self._list.count())
            if self._list.item(i).checkState() == Qt.CheckState.Checked
        ]
