// Entry point of the panel-material-ui bundle. Every component compiled into
// the bundle is registered under its class name, wrapped in the transforms
// listed in its _esm_transforms (kept in sync by tests/test_bundle.py).
// The remaining exports are shared with MaterialUIComponent subclasses
// through the shims in dist/.
import * as React from "react"
import {createRoot} from "react-dom/client"
import createCache from "@emotion/cache"
import {CacheProvider} from "@emotion/react"
import * as react_is from "react-is"
import * as react_dom from "react-dom"
import {jsx, jsxs, Fragment} from "react/jsx-runtime"
import * as material_styles from "@mui/material/styles"
import * as material_ui from "@mui/material"
import {apply_global_css, install_theme_hooks} from "./utils"
import {component, withLoading, withTheme, withTooltip} from "./transforms"

import {render as NotificationArea} from "./NotificationArea"
import {render as ChatArea} from "./chat/ChatArea"
import {render as ChatMessage} from "./chat/ChatMessage"
import {render as ChatStep} from "./chat/ChatStep"
import {render as Accordion} from "./layout/Accordion"
import {render as Alert} from "./layout/Alert"
import {render as Backdrop} from "./layout/Backdrop"
import {render as Box} from "./layout/Box"
import {render as Card} from "./layout/Card"
import {render as Container} from "./layout/Container"
import {render as Details} from "./layout/Details"
import {render as Dialog} from "./layout/Dialog"
import {render as Divider} from "./layout/Divider"
import {render as Drawer} from "./layout/Drawer"
import {render as Feed} from "./layout/Feed"
import {render as FloatPanel} from "./layout/FloatPanel"
import {render as Grid} from "./layout/Grid"
import {render as Paper} from "./layout/Paper"
import {render as Popup} from "./layout/Popup"
import {render as Tabs} from "./layout/Tabs"
import {render as Typography} from "./pane/Typography"
import {render as AppBar} from "./template/AppBar"
import {render as BreakpointSwitcher} from "./template/BreakpointSwitcher"
import {render as Page} from "./template/Page"
import {render as ThemeToggle} from "./template/ThemeToggle"
import {render as Autocomplete} from "./widgets/Autocomplete"
import {render as Avatar} from "./widgets/Avatar"
import {render as Breadcrumbs} from "./widgets/Breadcrumbs"
import {render as Button} from "./widgets/Button"
import {render as ButtonGroup} from "./widgets/ButtonGroup"
import {render as Checkbox} from "./widgets/Checkbox"
import {render as Chip} from "./widgets/Chip"
import {render as CircularProgress} from "./widgets/CircularProgress"
import {render as ColorMap} from "./widgets/ColorMap"
import {render as ColorPicker} from "./widgets/ColorPicker"
import {render as CrossSelector} from "./widgets/CrossSelector"
import {render as DateRangePicker} from "./widgets/DateRangePicker"
import {render as DateTimePicker} from "./widgets/DateTimePicker"
import {render as Fab} from "./widgets/Fab"
import {render as FileDownload} from "./widgets/FileDownload"
import {render as FileInput} from "./widgets/FileInput"
import {render as FileSelector} from "./widgets/FileSelector"
import {render as IconButton} from "./widgets/IconButton"
import {render as LinearProgress} from "./widgets/LinearProgress"
import {render as List} from "./widgets/List"
import {render as MenuBar} from "./widgets/MenuBar"
import {render as MenuButton} from "./widgets/MenuButton"
import {render as MenuToggle} from "./widgets/MenuToggle"
import {render as MultiSelect} from "./widgets/MultiSelect"
import {render as NestedBreadcrumbs} from "./widgets/NestedBreadcrumbs"
import {render as NumberInput} from "./widgets/NumberInput"
import {render as Pagination} from "./widgets/Pagination"
import {render as PasswordField} from "./widgets/PasswordField"
import {render as Pill} from "./widgets/Pill"
import {render as Player} from "./widgets/Player"
import {render as RadioGroup} from "./widgets/RadioGroup"
import {render as Rating} from "./widgets/Rating"
import {render as Select} from "./widgets/Select"
import {render as Slider} from "./widgets/Slider"
import {render as SpeedDial} from "./widgets/SpeedDial"
import {render as SplitButton} from "./widgets/SplitButton"
import {render as StaticText} from "./widgets/StaticText"
import {render as StepperMenu} from "./widgets/StepperMenu"
import {render as Switch} from "./widgets/Switch"
import {render as TabMenu} from "./widgets/TabMenu"
import {render as TextArea} from "./widgets/TextArea"
import {render as TextField} from "./widgets/TextField"
import {render as TimePicker} from "./widgets/TimePicker"
import {render as ToggleButton} from "./widgets/ToggleButton"
import {render as ToggleIcon} from "./widgets/ToggleIcon"
import {render as Tree} from "./widgets/Tree"
import {render as Badge} from "./wrappers/Badge"
import {render as Clickable} from "./wrappers/Clickable"
import {render as Skeleton} from "./wrappers/Skeleton"
import {render as Tooltip} from "./wrappers/Tooltip"
import {render as Transition} from "./wrappers/Transition"

export default {
  ChatAreaInput: component(ChatArea, withTheme),
  ChatMessage: component(ChatMessage, withLoading, withTheme),
  ChatStep: component(ChatStep, withLoading, withTheme),
  Accordion: component(Accordion, withLoading, withTheme),
  Alert: component(Alert, withLoading, withTheme),
  Backdrop: component(Backdrop, withLoading, withTheme),
  Card: component(Card, withLoading, withTheme),
  Column: component(Box, withLoading, withTheme),
  Container: component(Container, withLoading, withTheme),
  Details: component(Details, withLoading, withTheme),
  Dialog: component(Dialog, withLoading, withTheme),
  Divider: component(Divider, withLoading, withTheme),
  Drawer: component(Drawer, withLoading, withTheme),
  Feed: component(Feed, withLoading, withTheme),
  FlexBox: component(Box, withLoading, withTheme),
  FloatPanel: component(FloatPanel, withLoading, withTheme),
  Grid: component(Grid, withLoading, withTheme),
  Paper: component(Paper, withLoading, withTheme),
  Popup: component(Popup, withLoading, withTheme),
  Row: component(Box, withLoading, withTheme),
  Tabs: component(Tabs, withLoading, withTheme),
  NotificationArea: component(NotificationArea, withLoading, withTheme),
  DatetimeInput: component(TextField, withLoading, withTheme),
  DiscreteSlider: component(Slider, withLoading, withTheme),
  EditableFloatSlider: component(Slider, withLoading, withTheme),
  EditableIntSlider: component(Slider, withLoading, withTheme),
  FloatSlider: component(Slider, withLoading, withTheme),
  IntSlider: component(Slider, withLoading, withTheme),
  Player: component(Player, withLoading, withTheme),
  Select: component(Select, withLoading, withTheme),
  Typography: component(Typography, withLoading, withTheme),
  AppBar: component(AppBar, withLoading, withTheme),
  BreakpointSwitcher: component(BreakpointSwitcher, withLoading, withTheme),
  Page: component(Page, withLoading, withTheme),
  ThemeToggle: component(ThemeToggle, withTheme),
  Button: component(Button, withTooltip, withTheme),
  Chip: component(Chip, withTooltip, withTheme),
  Fab: component(Fab, withTooltip, withTheme),
  Toggle: component(ToggleButton, withLoading, withTooltip, withTheme),
  ColorMap: component(ColorMap, withLoading, withTheme),
  FileSelector: component(FileSelector, withLoading, withTheme),
  Avatar: component(Avatar, withLoading, withTheme),
  IconButton: component(IconButton, withTooltip, withLoading, withTheme),
  ToggleIcon: component(ToggleIcon, withTooltip, withLoading, withTheme),
  CircularProgress: component(CircularProgress, withTheme),
  LinearProgress: component(LinearProgress, withTheme),
  TextInput: component(TextField, withLoading, withTheme),
  PasswordInput: component(PasswordField, withLoading, withTheme),
  TextAreaInput: component(TextArea, withLoading, withTheme),
  FileInput: component(FileInput, withTooltip, withTheme),
  IntInput: component(NumberInput, withLoading, withTheme),
  FloatInput: component(NumberInput, withLoading, withTheme),
  NumberInput: component(NumberInput, withLoading, withTheme),
  DatePicker: component(DateTimePicker, withLoading, withTheme),
  DateRangePicker: component(DateRangePicker, withLoading, withTheme),
  DatetimeRangePicker: component(DateRangePicker, withLoading, withTheme),
  DatetimePicker: component(DateTimePicker, withLoading, withTheme),
  TimePicker: component(TimePicker, withLoading, withTheme),
  Checkbox: component(Checkbox, withLoading, withTheme),
  Switch: component(Switch, withLoading, withTheme),
  ColorPicker: component(ColorPicker, withLoading, withTheme),
  StaticText: component(StaticText, withLoading, withTheme),
  LiteralInput: component(TextField, withLoading, withTheme),
  ArrayInput: component(TextField, withLoading, withTheme),
  DictInput: component(TextField, withLoading, withTheme),
  ListInput: component(TextField, withLoading, withTheme),
  TupleInput: component(TextField, withLoading, withTheme),
  Breadcrumbs: component(Breadcrumbs, withLoading, withTheme),
  MenuBar: component(MenuBar, withLoading, withTheme),
  MenuButton: component(MenuButton, withTooltip, withTheme),
  MenuList: component(List, withLoading, withTheme),
  MenuToggle: component(MenuToggle, withTooltip, withTheme),
  NestedBreadcrumbs: component(NestedBreadcrumbs, withLoading, withTheme),
  Pagination: component(Pagination, withLoading, withTheme),
  SpeedDial: component(SpeedDial, withLoading, withTheme),
  SplitButton: component(SplitButton, withTooltip, withTheme),
  StepperMenu: component(StepperMenu, withLoading, withTheme),
  TabMenu: component(TabMenu, withLoading, withTheme),
  Tree: component(Tree, withLoading, withTheme),
  FileDownload: component(FileDownload, withTooltip, withTheme),
  DiscretePlayer: component(Player, withLoading, withTheme),
  AutocompleteInput: component(Autocomplete, withLoading, withTheme),
  CrossSelector: component(CrossSelector, withLoading, withTheme),
  RadioBoxGroup: component(RadioGroup, withLoading, withTheme),
  CheckBoxGroup: component(RadioGroup, withLoading, withTheme),
  RadioButtonGroup: component(ButtonGroup, withLoading, withTheme),
  CheckButtonGroup: component(ButtonGroup, withLoading, withTheme),
  MultiSelect: component(MultiSelect, withLoading, withTheme),
  MultiChoice: component(Select, withLoading, withTheme),
  Pill: component(Pill, withLoading, withTheme),
  MultiPill: component(Pill, withLoading, withTheme),
  DateSlider: component(Slider, withLoading, withTheme),
  DatetimeSlider: component(Slider, withLoading, withTheme),
  DateRangeSlider: component(Slider, withLoading, withTheme),
  DatetimeRangeSlider: component(Slider, withLoading, withTheme),
  EditableRangeSlider: component(Slider, withLoading, withTheme),
  EditableIntRangeSlider: component(Slider, withLoading, withTheme),
  IntRangeSlider: component(Slider, withLoading, withTheme),
  RangeSlider: component(Slider, withLoading, withTheme),
  Rating: component(Rating, withLoading, withTheme),
  Clickable: component(Clickable, withLoading, withTheme),
  Transition: component(Transition, withLoading, withTheme),
  Badge: component(Badge, withLoading, withTheme),
  Skeleton: component(Skeleton, withLoading, withTheme),
  Tooltip: component(Tooltip, withLoading, withTheme),
  React,
  createRoot,
  createCache,
  CacheProvider,
  react_is,
  react_dom,
  jsx,
  jsxs,
  Fragment,
  apply_global_css,
  install_theme_hooks,
  material_styles,
  material_ui,
  withLoading,
  withTheme,
  withTooltip,
}
