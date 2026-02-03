# Release Notes

## Version 0.9.0

This release includes enhancements, bug fixes, and documentation updates.

### ✨ Enhancements

- Add support for providing tooltip for menu items ([#570](https://github.com/panel-extensions/panel-material-ui/pull/570))
- Support icon shorthand for all widgets and menus ([#569](https://github.com/panel-extensions/panel-material-ui/pull/569))
- Add `Pill` and `MultiPill` widgets ([#568](https://github.com/panel-extensions/panel-material-ui/pull/568))
- Allow providing Theme overrides ([#565](https://github.com/panel-extensions/panel-material-ui/pull/565))
- Add ability to disable link on click in `MenuList` ([#560](https://github.com/panel-extensions/panel-material-ui/pull/560))

### 🐛 Bug Fixes

- Fix `MaterialUIComponent` ([#566](https://github.com/panel-extensions/panel-material-ui/pull/566))
- Ensure `icon_size` overrides standard size ([#556](https://github.com/panel-extensions/panel-material-ui/pull/556))

### 📚 Documentation

- Document how to use custom icons in MaterialUIComponent ([#571](https://github.com/panel-extensions/panel-material-ui/pull/571))
- Improve how-to indexing and titles ([#567](https://github.com/panel-extensions/panel-material-ui/pull/567))

## Version 0.8.1

This release includes enhancements, documentation updates, and developer/infrastructure improvements.

### ✨ Enhancements

- Unify Icon rendering ([#555](https://github.com/panel-extensions/panel-material-ui/pull/555))
- Add sync method to `ChatAreaInput` ([#552](https://github.com/panel-extensions/panel-material-ui/pull/552))
- Expose `SpeedDial.size` ([#554](https://github.com/panel-extensions/panel-material-ui/pull/554))
- Tweak styles ([#553](https://github.com/panel-extensions/panel-material-ui/pull/553))

### 🧪 Infrastructure & Developer Experience

- Bump the gh-actions group with 2 updates ([#549](https://github.com/panel-extensions/panel-material-ui/pull/549))

## Version 0.8.0

This release includes enhancements, bug fixes, developer/infrastructure improvements, and additional changes.

### ✨ Enhancements

- Padding and sizing adjustments for MenuList, Accordion and CrossSelector ([#544](https://github.com/panel-extensions/panel-material-ui/pull/544))
- Implement new Details layout ([#533](https://github.com/panel-extensions/panel-material-ui/pull/533))
- Add support for TextAreaInput.enter_pressed ([#537](https://github.com/panel-extensions/panel-material-ui/pull/537))
- Reduce margin on Page theme toggle ([#536](https://github.com/panel-extensions/panel-material-ui/pull/536))
- Add Menu.update_item method ([#522](https://github.com/panel-extensions/panel-material-ui/pull/522))
- Implement MenuList.collapsed for condensed menu ([#519](https://github.com/panel-extensions/panel-material-ui/pull/519))
- EditableSlider UI/UX improvements ([#501](https://github.com/panel-extensions/panel-material-ui/pull/501))
- LoadingTransform UI/UX improvements ([#503](https://github.com/panel-extensions/panel-material-ui/pull/503))
- Add FileDownload.transfer method ([#515](https://github.com/panel-extensions/panel-material-ui/pull/515))

### 🐛 Bug Fixes

- Ensure mime types are set for woff font files ([#546](https://github.com/panel-extensions/panel-material-ui/pull/546))
- Fix Button variant documentation ([#538](https://github.com/panel-extensions/panel-material-ui/pull/538))
- Fix CheckBox/RadioBoxGroup widgets error in components.py and update docs ([#527](https://github.com/panel-extensions/panel-material-ui/pull/527))
- Ensure ChatMessage header and footer objects are rendered ([#530](https://github.com/panel-extensions/panel-material-ui/pull/530))
- Fix missing loading_inset on Column/Row ([#524](https://github.com/panel-extensions/panel-material-ui/pull/524))
- Correctly handle different Icon variants ([#521](https://github.com/panel-extensions/panel-material-ui/pull/521))
- Ensure NestedBreadcrumbs path does not override active ([#517](https://github.com/panel-extensions/panel-material-ui/pull/517))

### 🧪 Infrastructure & Developer Experience

- Bump the gh-actions group with 2 updates ([#516](https://github.com/panel-extensions/panel-material-ui/pull/516))

### 🗂️ Other

- Animate Page sidebar collapse ([#545](https://github.com/panel-extensions/panel-material-ui/pull/545))
- Reset Tabs min-height after transition ([#523](https://github.com/panel-extensions/panel-material-ui/pull/523))
- Always apply ChatMessage style overrides ([#520](https://github.com/panel-extensions/panel-material-ui/pull/520))

## Version 0.7.0

This release includes enhancements, bug fixes, and developer/infrastructure improvements.

### ✨ Enhancements

- Improve Tabs height transitions ([#514](https://github.com/panel-extensions/panel-material-ui/pull/514))
- Reduce padding ([#513](https://github.com/panel-extensions/panel-material-ui/pull/513))
- Add TabMenu component ([#511](https://github.com/panel-extensions/panel-material-ui/pull/511))
- Add MenuList and Tree toggle_action ([#509](https://github.com/panel-extensions/panel-material-ui/pull/509))
- Add lazy_search to AutocompleteInput ([#507](https://github.com/panel-extensions/panel-material-ui/pull/507))
- Add Tree Menu component ([#506](https://github.com/panel-extensions/panel-material-ui/pull/506))
- Adjust theming of some components ([#505](https://github.com/panel-extensions/panel-material-ui/pull/505))
- Implement attached views anchored to the parent ([#174](https://github.com/panel-extensions/panel-material-ui/pull/174))
- Add Widget.focus() method ([#504](https://github.com/panel-extensions/panel-material-ui/pull/504))

### 🐛 Bug Fixes

- Ensure focus callback is registered once and cleaned up ([#510](https://github.com/panel-extensions/panel-material-ui/pull/510))
- Fix NestedBreadcrumbs UI test on windows ([#508](https://github.com/panel-extensions/panel-material-ui/pull/508))

### 🧪 Infrastructure & Developer Experience

- Bump panel-material-ui version to 7.3.5 ([#512](https://github.com/panel-extensions/panel-material-ui/pull/512))

## Version 0.6.0

This release includes enhancements, bug fixes, developer/infrastructure improvements, and additional changes.

### ✨ Enhancements

- FileDownload UI/UX improvements ([#496](https://github.com/panel-extensions/panel-material-ui/pull/496))
- Add MenuList.show_children parameter ([#494](https://github.com/panel-extensions/panel-material-ui/pull/494))
- Do not attempt to jslink parameters that do not support it ([#493](https://github.com/panel-extensions/panel-material-ui/pull/493))
- Add draggable/resizable sidebar functionality to MUI Drawer-based sidebar ([#476](https://github.com/panel-extensions/panel-material-ui/pull/476))
- Add NestedBreadcrumbs menu component ([#488](https://github.com/panel-extensions/panel-material-ui/pull/488))
- MenuList UX/UI improvements ([#486](https://github.com/panel-extensions/panel-material-ui/pull/486))

### 🐛 Bug Fixes

- Fix initialization of ChatMessage.avatar param ([#498](https://github.com/panel-extensions/panel-material-ui/pull/498))
- Various fixes to avoid parameter de-referencing ([#495](https://github.com/panel-extensions/panel-material-ui/pull/495))
- Ensure provided Menu value is not overridden by None active value ([#492](https://github.com/panel-extensions/panel-material-ui/pull/492))
- Ensure adding ThemeToggle to an app enables managed theme support ([#491](https://github.com/panel-extensions/panel-material-ui/pull/491))
- Fix ChatArea status_ref handling ([#490](https://github.com/panel-extensions/panel-material-ui/pull/490))
- Fix TextArea.auto_grow ([#489](https://github.com/panel-extensions/panel-material-ui/pull/489))

### 🧪 Infrastructure & Developer Experience

- chore: Update pre-commit and fixes ([#502](https://github.com/panel-extensions/panel-material-ui/pull/502))
- Bump the gh-actions group with 4 updates ([#487](https://github.com/panel-extensions/panel-material-ui/pull/487))

### 🗂️ Other

- Remove button label as a link for FileDownload button when auto is False ([#500](https://github.com/panel-extensions/panel-material-ui/pull/500))
- Clear ChatAreaInput status ref before removal ([#499](https://github.com/panel-extensions/panel-material-ui/pull/499))

## Version 0.5.1

This release includes enhancements, bug fixes, and developer/infrastructure improvements.

### ✨ Enhancements

- Align Button icon_size ([#473](https://github.com/panel-extensions/panel-material-ui/pull/473))
- Expose control over Accordion, Card, Dialog title_variant ([#472](https://github.com/panel-extensions/panel-material-ui/pull/472))
- enh: Improve FileInput ([#471](https://github.com/panel-extensions/panel-material-ui/pull/471))

### 🐛 Bug Fixes

- Ensure TextAreaInput height is respected ([#474](https://github.com/panel-extensions/panel-material-ui/pull/474))

### 🧪 Infrastructure & Developer Experience

- Bump the gh-actions group across 1 directory with 5 updates ([#478](https://github.com/panel-extensions/panel-material-ui/pull/478))

## Version 0.5.0

This release includes enhancements, bug fixes, documentation updates, developer/infrastructure improvements, and additional changes.

### ✨ Enhancements

- Register HoloViews widgets and template ([#469](https://github.com/panel-extensions/panel-material-ui/pull/469))
- Reduce Accordion padding ([#468](https://github.com/panel-extensions/panel-material-ui/pull/468))
- Implement TextArea.resizable ([#436](https://github.com/panel-extensions/panel-material-ui/pull/436))
- Update to Mui v7 ([#459](https://github.com/panel-extensions/panel-material-ui/pull/459))
- enh: Add size to CrossSelector ([#456](https://github.com/panel-extensions/panel-material-ui/pull/456))
- Implement support for reconnect notifications ([#444](https://github.com/panel-extensions/panel-material-ui/pull/444))
- Improve upload progress reporting ([#458](https://github.com/panel-extensions/panel-material-ui/pull/458))
- Minor Chat tweaks ([#451](https://github.com/panel-extensions/panel-material-ui/pull/451))
- Improve ChatAreaInput's upload experience ([#440](https://github.com/panel-extensions/panel-material-ui/pull/440))
- Add border to active MenuList item ([#449](https://github.com/panel-extensions/panel-material-ui/pull/449))
- Implement IconButton href and target ([#435](https://github.com/panel-extensions/panel-material-ui/pull/435))
- Align button menu components ([#425](https://github.com/panel-extensions/panel-material-ui/pull/425))

### 🐛 Bug Fixes

- Fix href support on MenuButton items ([#467](https://github.com/panel-extensions/panel-material-ui/pull/467))
- Ensure FileDownload fetches latest data ([#464](https://github.com/panel-extensions/panel-material-ui/pull/464))
- Fix default item open state handling in List component #454 ([#455](https://github.com/panel-extensions/panel-material-ui/pull/455))
- Ensure CSS icon_size is permitted on IconButton and ToggleIcon ([#453](https://github.com/panel-extensions/panel-material-ui/pull/453))
- Fix Dialog padding and close button alignment ([#452](https://github.com/panel-extensions/panel-material-ui/pull/452))
- Fix Accordion header color ([#447](https://github.com/panel-extensions/panel-material-ui/pull/447))
- Revert "Ensure material-variables CSS does not override font and color" ([#419](https://github.com/panel-extensions/panel-material-ui/pull/419)) ([#445](https://github.com/panel-extensions/panel-material-ui/pull/445))
- Ensure components in header adapt to header color ([#438](https://github.com/panel-extensions/panel-material-ui/pull/438))
- Ensure Select outlined variant is notched when updating value ([#434](https://github.com/panel-extensions/panel-material-ui/pull/434))

### 📚 Documentation

- Align documentation of color variants ([#450](https://github.com/panel-extensions/panel-material-ui/pull/450))

### 🧪 Infrastructure & Developer Experience

- Register CDN and dist directory with panel ([#463](https://github.com/panel-extensions/panel-material-ui/pull/463))

### 🗂️ Other

- Replace pyodide loader ([#466](https://github.com/panel-extensions/panel-material-ui/pull/466))
- Update `mui.py` for page.meta changes ([#441](https://github.com/panel-extensions/panel-material-ui/pull/441))
- Trigger send event if sending empty message with uploaded files ([#460](https://github.com/panel-extensions/panel-material-ui/pull/460))
- Wait to send ChatAreaInput message until files are uploaded ([#457](https://github.com/panel-extensions/panel-material-ui/pull/457))
- Portal tooltips into Page root ([#439](https://github.com/panel-extensions/panel-material-ui/pull/439))
- Hide selected options in MultiChoice option list ([#432](https://github.com/panel-extensions/panel-material-ui/pull/432))

## Version 0.4.0

This release includes enhancements, bug fixes, documentation updates, and additional changes.

### ✨ Enhancements

- Add missing notebooks ([#368](https://github.com/panel-extensions/panel-material-ui/pull/368))
- Add MenuToggle ([#406](https://github.com/panel-extensions/panel-material-ui/pull/406))
- Align IconButton and ToggleIcon sizing ([#411](https://github.com/panel-extensions/panel-material-ui/pull/411))
- Allow rendering components into Accordion and Tabs headers ([#409](https://github.com/panel-extensions/panel-material-ui/pull/409))
- Add input params ([#401](https://github.com/panel-extensions/panel-material-ui/pull/401))
- Make adjustments to font-size after changing defaults ([#404](https://github.com/panel-extensions/panel-material-ui/pull/404))
- Optimize font CSS lookups ([#399](https://github.com/panel-extensions/panel-material-ui/pull/399))
- Add `SplitButton` widget ([#284](https://github.com/panel-extensions/panel-material-ui/pull/284))
- Reduce default Typography header size ([#394](https://github.com/panel-extensions/panel-material-ui/pull/394))
- Allow setting open on MenuList items ([#395](https://github.com/panel-extensions/panel-material-ui/pull/395))
- Consistently support Widget.description tooltips ([#393](https://github.com/panel-extensions/panel-material-ui/pull/393))

### 🐛 Bug Fixes

- Ensure material-variables CSS does not override font and color ([#419](https://github.com/panel-extensions/panel-material-ui/pull/419))
- fix link ([#415](https://github.com/panel-extensions/panel-material-ui/pull/415))
- Handle sync of MuiNotification model ([#412](https://github.com/panel-extensions/panel-material-ui/pull/412))
- Fix handling of decimal values in NumberInput validation ([#413](https://github.com/panel-extensions/panel-material-ui/pull/413))
- Ensure classic panel components are styled correctly ([#408](https://github.com/panel-extensions/panel-material-ui/pull/408))
- Fix regression adding items to MenuList ([#396](https://github.com/panel-extensions/panel-material-ui/pull/396))

### 📚 Documentation

- Review SplitButton Reference Guide ([#398](https://github.com/panel-extensions/panel-material-ui/pull/398))

### 🗂️ Other

- Change ChatMessage placeholder loading animation ([#417](https://github.com/panel-extensions/panel-material-ui/pull/417))
- Switch to outlined info icon for description ([#414](https://github.com/panel-extensions/panel-material-ui/pull/414))
- More alignment of component title sizes ([#410](https://github.com/panel-extensions/panel-material-ui/pull/410))
- Only jslink on Widget instances, not WidgetBase ([#390](https://github.com/panel-extensions/panel-material-ui/pull/390))

## Version 0.3.3

This release includes enhancements and bug fixes.

### ✨ Enhancements

- Allow switching Page.logo based on theme ([#388](https://github.com/panel-extensions/panel-material-ui/pull/388))

### 🐛 Bug Fixes

- Ensure FileDownload filename can be set inside callback ([#386](https://github.com/panel-extensions/panel-material-ui/pull/386))
- Ensure Select menu in notebook is scrollable ([#385](https://github.com/panel-extensions/panel-material-ui/pull/385))

## Version 0.3.2

This release includes bug fixes and documentation updates.

### 🐛 Bug Fixes

- Ensure icon_size is not dropped ([#384](https://github.com/panel-extensions/panel-material-ui/pull/384))
- Ensure Card and ChatStep titles wrap ([#383](https://github.com/panel-extensions/panel-material-ui/pull/383))

### 📚 Documentation

- Update Backdrop.ipynb text ([#381](https://github.com/panel-extensions/panel-material-ui/pull/381))

## Version 0.3.1

This release includes bug fixes, documentation updates, developer/infrastructure improvements, and additional changes.

### 🐛 Bug Fixes

- Fix bug when clearing Tabs ([#374](https://github.com/panel-extensions/panel-material-ui/pull/374))
- Fix textual issue in icons.md ([#369](https://github.com/panel-extensions/panel-material-ui/pull/369))

### 📚 Documentation

- Add link in components.md doc ([#370](https://github.com/panel-extensions/panel-material-ui/pull/370))
- Add missing doc attributes ([#365](https://github.com/panel-extensions/panel-material-ui/pull/365))

### 🧪 Infrastructure & Developer Experience

- Add support for toggle actions on MenuList ([#376](https://github.com/panel-extensions/panel-material-ui/pull/376))

### 🗂️ Other

- Hide empty Tabs ([#377](https://github.com/panel-extensions/panel-material-ui/pull/377))
- Wrap EditableSlider label ([#373](https://github.com/panel-extensions/panel-material-ui/pull/373))

## Version 0.3.0

This release includes enhancements, bug fixes, documentation updates, developer/infrastructure improvements, and additional changes.

### ✨ Enhancements

- Minor 0.3 improvements ([#364](https://github.com/panel-extensions/panel-material-ui/pull/364))
- Implement file upload on ChatAreaInput ([#360](https://github.com/panel-extensions/panel-material-ui/pull/360))
- Add CrossSelector widget ([#355](https://github.com/panel-extensions/panel-material-ui/pull/355))
- Improve rendering Select and MenuButton in notebooks ([#340](https://github.com/panel-extensions/panel-material-ui/pull/340))
- Add pmui Plotly support ([#341](https://github.com/panel-extensions/panel-material-ui/pull/341))
- add typography color ([#352](https://github.com/panel-extensions/panel-material-ui/pull/352))
- Rename Progress and LoadingSpinner ([#338](https://github.com/panel-extensions/panel-material-ui/pull/338))
- Rename List to MenuList ([#336](https://github.com/panel-extensions/panel-material-ui/pull/336))
- Improve handling of Page.meta ([#332](https://github.com/panel-extensions/panel-material-ui/pull/332))
- Align TextInput, PasswordInput and AutocompleteInput ([#322](https://github.com/panel-extensions/panel-material-ui/pull/322))
- Align AutoCompleteInput-DatePicker with guiding principles ([#309](https://github.com/panel-extensions/panel-material-ui/pull/309))

### 🐛 Bug Fixes

- Ensure MenuList.active is stable ([#361](https://github.com/panel-extensions/panel-material-ui/pull/361))
- fix card collapsed ([#359](https://github.com/panel-extensions/panel-material-ui/pull/359))
- Fix updates to Typography pane ([#353](https://github.com/panel-extensions/panel-material-ui/pull/353))
- Fix Page header_color ([#329](https://github.com/panel-extensions/panel-material-ui/pull/329))

### 📚 Documentation

- Add pane reference guides ([#358](https://github.com/panel-extensions/panel-material-ui/pull/358))
- Documentation Review for 0.3.0 release ([#357](https://github.com/panel-extensions/panel-material-ui/pull/357))
- Cleanup of Menu reference docs ([#356](https://github.com/panel-extensions/panel-material-ui/pull/356))
- Add pane reference guides ([#354](https://github.com/panel-extensions/panel-material-ui/pull/354))
- Review Container reference ([#337](https://github.com/panel-extensions/panel-material-ui/pull/337))
- Update NestedSelect doc to indicate examples only work after Notebook execution ([#323](https://github.com/panel-extensions/panel-material-ui/pull/323))
- Branding ([#328](https://github.com/panel-extensions/panel-material-ui/pull/328))
- Review FileDownload and Fab widget ([#334](https://github.com/panel-extensions/panel-material-ui/pull/334))
- Align slider reference docs ([#335](https://github.com/panel-extensions/panel-material-ui/pull/335))
- Review TimePicker ([#333](https://github.com/panel-extensions/panel-material-ui/pull/333))
- Implement Dialog.show_close_button and update docs ([#331](https://github.com/panel-extensions/panel-material-ui/pull/331))
- Review Switch, Toggle, ToggleIcon and CheckBox ([#326](https://github.com/panel-extensions/panel-material-ui/pull/326))
- Review Indicators ([#316](https://github.com/panel-extensions/panel-material-ui/pull/316))
- Update TextInput.ipynb to removed the word 'obfuscated' ([#319](https://github.com/panel-extensions/panel-material-ui/pull/319))
- Update Button.ipynb to change section name and minor textual change ([#313](https://github.com/panel-extensions/panel-material-ui/pull/313))
- Update Switch.ipynb to mention it is interchangeable not only with Toggle, but also with Checkbox ([#315](https://github.com/panel-extensions/panel-material-ui/pull/315))

### 🧪 Infrastructure & Developer Experience

- expose compile-dev ([#363](https://github.com/panel-extensions/panel-material-ui/pull/363))

### 🗂️ Other

- Enhance ChatAreaInput ([#362](https://github.com/panel-extensions/panel-material-ui/pull/362))
- api tab names ([#311](https://github.com/panel-extensions/panel-material-ui/pull/311))

## Version 0.2.0

This release includes enhancements, bug fixes, documentation updates, and developer/infrastructure improvements.

### ✨ Enhancements

- Support href and target on MenuButton ([#302](https://github.com/panel-extensions/panel-material-ui/pull/302))
- Implement EditableRangeSliders ([#299](https://github.com/panel-extensions/panel-material-ui/pull/299))

### 🐛 Bug Fixes

- Correctly resolve themes and set default primary color ([#301](https://github.com/panel-extensions/panel-material-ui/pull/301))
- Fix conda install instructions ([#300](https://github.com/panel-extensions/panel-material-ui/pull/300))
- Fix FileInput not working ([#287](https://github.com/panel-extensions/panel-material-ui/pull/287))

### 📚 Documentation

- Consistently use Mui API in reference guide ([#305](https://github.com/panel-extensions/panel-material-ui/pull/305))
- Add ThemeToggle reference page ([#304](https://github.com/panel-extensions/panel-material-ui/pull/304))
- Reference doc alignment ([#303](https://github.com/panel-extensions/panel-material-ui/pull/303))
- Review CheckBoxGroup ([#297](https://github.com/panel-extensions/panel-material-ui/pull/297))
- Review follow up ([#296](https://github.com/panel-extensions/panel-material-ui/pull/296))
- Review Checkbox ([#293](https://github.com/panel-extensions/panel-material-ui/pull/293))
- Review AutocompleteInput ([#291](https://github.com/panel-extensions/panel-material-ui/pull/291))

### 🧪 Infrastructure & Developer Experience

- Reorganize and add Menu tests ([#295](https://github.com/panel-extensions/panel-material-ui/pull/295))
- Reorganize and add tests ([#294](https://github.com/panel-extensions/panel-material-ui/pull/294))
- Add support for List inline actions ([#292](https://github.com/panel-extensions/panel-material-ui/pull/292))

## Version 0.1.4

This release includes enhancements, bug fixes, documentation updates, and additional changes.

### ✨ Enhancements

- Allow setting Select size variant ([#286](https://github.com/panel-extensions/panel-material-ui/pull/286))

### 🐛 Bug Fixes

- Fix FileInput rendering of progress ([#279](https://github.com/panel-extensions/panel-material-ui/pull/279))

### 📚 Documentation

- FileInput Guide Review ([#278](https://github.com/panel-extensions/panel-material-ui/pull/278))

### 🗂️ Other

- Embed iframe content using srcdoc attribute for compatibility ([#285](https://github.com/panel-extensions/panel-material-ui/pull/285))

## Version 0.1.3

This release includes additional changes.

### 🗂️ Other

- Correctly determine sizing_mode on Page ([#276](https://github.com/panel-extensions/panel-material-ui/pull/276))

## Version 0.1.2

This release includes documentation updates.

### 📚 Documentation

- Adjust header of demo example ([#275](https://github.com/panel-extensions/panel-material-ui/pull/275))

## Version 0.1.1

This release includes additional changes.

### 🗂️ Other

- slider color primary ([#273](https://github.com/panel-extensions/panel-material-ui/pull/273))

## Version 0.1.0

This release includes enhancements, bug fixes, documentation updates, developer/infrastructure improvements, and additional changes.

### ✨ Enhancements

- Add Page.site_url option ([#268](https://github.com/panel-extensions/panel-material-ui/pull/268))
- Card padding tweaks ([#265](https://github.com/panel-extensions/panel-material-ui/pull/265))
- Align IconButton and ToggleIcon sizing ([#264](https://github.com/panel-extensions/panel-material-ui/pull/264))
- Add Dialog.close_on_click ([#263](https://github.com/panel-extensions/panel-material-ui/pull/263))
- Allow HTML in Card, Accordion and Tabs titles ([#259](https://github.com/panel-extensions/panel-material-ui/pull/259))
- Add FlexBox layout ([#257](https://github.com/panel-extensions/panel-material-ui/pull/257))
- Allow providing different logos per breakpoint ([#255](https://github.com/panel-extensions/panel-material-ui/pull/255))
- Rename to IconButton (and keep ButtonIcon alias) ([#239](https://github.com/panel-extensions/panel-material-ui/pull/239))
- Various smaller tweaks ([#254](https://github.com/panel-extensions/panel-material-ui/pull/254))
- Allow Page to render local icons and logos ([#236](https://github.com/panel-extensions/panel-material-ui/pull/236))
- Add busy indicator to Page ([#235](https://github.com/panel-extensions/panel-material-ui/pull/235))
- Add BreakpointSwitcher ([#214](https://github.com/panel-extensions/panel-material-ui/pull/214))
- Align import abbreviation on pmui ([#203](https://github.com/panel-extensions/panel-material-ui/pull/203))
- Enable deep theme inheritance ([#197](https://github.com/panel-extensions/panel-material-ui/pull/197))
- Add flex layouts and handling and improve managed theme ([#196](https://github.com/panel-extensions/panel-material-ui/pull/196))
- Refactor theme inheritance and add standalone ThemeToggle ([#187](https://github.com/panel-extensions/panel-material-ui/pull/187))
- Add Drawer layout ([#184](https://github.com/panel-extensions/panel-material-ui/pull/184))
- Tweaks and fixes ([#178](https://github.com/panel-extensions/panel-material-ui/pull/178))
- Various cleanup ([#173](https://github.com/panel-extensions/panel-material-ui/pull/173))
- Improve handling of theme resources ([#163](https://github.com/panel-extensions/panel-material-ui/pull/163))
- Clean up and improve Indicators ([#162](https://github.com/panel-extensions/panel-material-ui/pull/162))
- Add Fab button ([#161](https://github.com/panel-extensions/panel-material-ui/pull/161))
- Allow providing href to Button ([#160](https://github.com/panel-extensions/panel-material-ui/pull/160))
- Clean up widgets and consistently define default palette ([#137](https://github.com/panel-extensions/panel-material-ui/pull/137))
- Align widget APIs ([#135](https://github.com/panel-extensions/panel-material-ui/pull/135))
- Improve ButtonIcon icon handling ([#130](https://github.com/panel-extensions/panel-material-ui/pull/130))
- Add customization guides ([#129](https://github.com/panel-extensions/panel-material-ui/pull/129))
- More fixes and cleanup of Select widget(s) ([#128](https://github.com/panel-extensions/panel-material-ui/pull/128))
- New widgets : SelectPicker and SelectSearch ([#107](https://github.com/panel-extensions/panel-material-ui/pull/107))
- Add theme inheritance ([#124](https://github.com/panel-extensions/panel-material-ui/pull/124))
- Implement MaterialComponent.loading using native loading spinner ([#122](https://github.com/panel-extensions/panel-material-ui/pull/122))
- Improve Menu API and functionality ([#117](https://github.com/panel-extensions/panel-material-ui/pull/117))
- Implement Page.meta to allow setting meta tags in template ([#114](https://github.com/panel-extensions/panel-material-ui/pull/114))
- Add Param patches ([#111](https://github.com/panel-extensions/panel-material-ui/pull/111))
- Add contextbar to Page ([#105](https://github.com/panel-extensions/panel-material-ui/pull/105))
- Unify theme handling ([#103](https://github.com/panel-extensions/panel-material-ui/pull/103))
- Add FileDownload widget ([#102](https://github.com/panel-extensions/panel-material-ui/pull/102))
- Minor cleanup of Select widgets ([#99](https://github.com/panel-extensions/panel-material-ui/pull/99))
- Implement Chat Components ([#100](https://github.com/panel-extensions/panel-material-ui/pull/100))
- Add a website ([#101](https://github.com/panel-extensions/panel-material-ui/pull/101))
- Implement Notifications ([#94](https://github.com/panel-extensions/panel-material-ui/pull/94))
- Add ColorPicker ([#92](https://github.com/panel-extensions/panel-material-ui/pull/92))
- Input widgets - implement missing features, bug fixes ([#82](https://github.com/panel-extensions/panel-material-ui/pull/82))
- Add global control over theme ([#83](https://github.com/panel-extensions/panel-material-ui/pull/83))
- Add Menu components ([#77](https://github.com/panel-extensions/panel-material-ui/pull/77))
- Improve Select and Slider components ([#71](https://github.com/panel-extensions/panel-material-ui/pull/71))
- Allow setting IntSlider.step ([#70](https://github.com/panel-extensions/panel-material-ui/pull/70))
- Unify DatePicker implementations ([#69](https://github.com/panel-extensions/panel-material-ui/pull/69))
- Update docstrings - add references ([#63](https://github.com/panel-extensions/panel-material-ui/pull/63))
- Implement bundling and add more components ([#50](https://github.com/panel-extensions/panel-material-ui/pull/50))

### 🐛 Bug Fixes

- Ensure flex styling is reapplied when update_layout is called ([#270](https://github.com/panel-extensions/panel-material-ui/pull/270))
- Ensure template is correctly resolved ([#269](https://github.com/panel-extensions/panel-material-ui/pull/269))
- Ensure components in Page follow flex sizing ([#250](https://github.com/panel-extensions/panel-material-ui/pull/250))
- Fix embedding of ico files on favicon ([#249](https://github.com/panel-extensions/panel-material-ui/pull/249))
- Ensure theme class is correctly replaced on toggle ([#244](https://github.com/panel-extensions/panel-material-ui/pull/244))
- Ensure Page manages the theme ([#243](https://github.com/panel-extensions/panel-material-ui/pull/243))
- Ensure temporary Drawer does not take up space ([#242](https://github.com/panel-extensions/panel-material-ui/pull/242))
- Ensure Select menu is correctly positioned in notebook ([#241](https://github.com/panel-extensions/panel-material-ui/pull/241))
- Ensure theme_config can toggle between dark and light themes ([#229](https://github.com/panel-extensions/panel-material-ui/pull/229))
- Resolve reported documentation issues ([#210](https://github.com/panel-extensions/panel-material-ui/pull/210))
- Fix rendering of ChatMessage avatar ([#182](https://github.com/panel-extensions/panel-material-ui/pull/182))
- Align theming and ensure variables are set ([#179](https://github.com/panel-extensions/panel-material-ui/pull/179))
- Ensure no race conditions and multiple rerenders on theme changes ([#172](https://github.com/panel-extensions/panel-material-ui/pull/172))
- Ensure ButtonIcon handles clicks ([#159](https://github.com/panel-extensions/panel-material-ui/pull/159))
- Consistently handle Widget labels and width ([#158](https://github.com/panel-extensions/panel-material-ui/pull/158))
- Fix SvgIcons ([#112](https://github.com/panel-extensions/panel-material-ui/pull/112))
- build: Fix small typo ([#113](https://github.com/panel-extensions/panel-material-ui/pull/113))
- Fix Checkbox alignment and width ([#98](https://github.com/panel-extensions/panel-material-ui/pull/98))
- Fix and improve FileInput ([#97](https://github.com/panel-extensions/panel-material-ui/pull/97))
- Fix theming if no theme_config provided ([#93](https://github.com/panel-extensions/panel-material-ui/pull/93))
- fix panel pin ([#91](https://github.com/panel-extensions/panel-material-ui/pull/91))
- Fix and improve layout components ([#84](https://github.com/panel-extensions/panel-material-ui/pull/84))
- Fix datetime picker ([#76](https://github.com/panel-extensions/panel-material-ui/pull/76))
- Fix text input ([#74](https://github.com/panel-extensions/panel-material-ui/pull/74))
- Fix time picker ([#75](https://github.com/panel-extensions/panel-material-ui/pull/75))
- Fix versioning ([#73](https://github.com/panel-extensions/panel-material-ui/pull/73))
- fix some dev guide issues ([#68](https://github.com/panel-extensions/panel-material-ui/pull/68))
- Fix versioning and CDN loading code ([#65](https://github.com/panel-extensions/panel-material-ui/pull/65))

### 📚 Documentation

- Use last defined document ([#256](https://github.com/panel-extensions/panel-material-ui/pull/256))
- Branded reference app ([#228](https://github.com/panel-extensions/panel-material-ui/pull/228))
- DiscreteSlider Follow Up Review ([#247](https://github.com/panel-extensions/panel-material-ui/pull/247))
- Button Follow Up Review ([#245](https://github.com/panel-extensions/panel-material-ui/pull/245))
- Select Review Feedback ([#234](https://github.com/panel-extensions/panel-material-ui/pull/234))
- DiscreteSlider Review ([#237](https://github.com/panel-extensions/panel-material-ui/pull/237))
- button docs ([#176](https://github.com/panel-extensions/panel-material-ui/pull/176))
- Fixes from non-reference docs review ([#216](https://github.com/panel-extensions/panel-material-ui/pull/216))
- Docstring reference improvements ([#219](https://github.com/panel-extensions/panel-material-ui/pull/219))
- add showcase ([#209](https://github.com/panel-extensions/panel-material-ui/pull/209))
- Add example to homepage ([#207](https://github.com/panel-extensions/panel-material-ui/pull/207))
- Document icon usage ([#204](https://github.com/panel-extensions/panel-material-ui/pull/204))
- Theming Refactor - HoloViews Example ([#191](https://github.com/panel-extensions/panel-material-ui/pull/191))
- Improve and document Page ([#185](https://github.com/panel-extensions/panel-material-ui/pull/185))
- Improve and document Notifications ([#181](https://github.com/panel-extensions/panel-material-ui/pull/181))
- Clean up chat and add docs ([#180](https://github.com/panel-extensions/panel-material-ui/pull/180))
- Clean up and document Menus ([#169](https://github.com/panel-extensions/panel-material-ui/pull/169))
- review feedback ([#134](https://github.com/panel-extensions/panel-material-ui/pull/134))
- Improve CDN setup in pyodide and docs ([#127](https://github.com/panel-extensions/panel-material-ui/pull/127))
- Move examples/reference/layout to examples/reference/layouts ([#126](https://github.com/panel-extensions/panel-material-ui/pull/126))
- Review and document layouts ([#125](https://github.com/panel-extensions/panel-material-ui/pull/125))
- Cleanup and review of all widgets ([#108](https://github.com/panel-extensions/panel-material-ui/pull/108))

### 🧪 Infrastructure & Developer Experience

- Bump prefix-dev/setup-pixi from 0.8.4 to 0.8.8 in the gh-actions group ([#220](https://github.com/panel-extensions/panel-material-ui/pull/220))
- Bump panel and bokeh versions ([#271](https://github.com/panel-extensions/panel-material-ui/pull/271))
- Add more menu tests ([#199](https://github.com/panel-extensions/panel-material-ui/pull/199))
- Allow creating custom MaterialComponents using bundle shims ([#177](https://github.com/panel-extensions/panel-material-ui/pull/177))
- Bump prefix-dev/setup-pixi from 0.8.3 to 0.8.4 in the gh-actions group ([#115](https://github.com/panel-extensions/panel-material-ui/pull/115))
- Add Page.config to add resources ([#116](https://github.com/panel-extensions/panel-material-ui/pull/116))
- Bump the gh-actions group with 3 updates ([#79](https://github.com/panel-extensions/panel-material-ui/pull/79))
- Simplify pixi installation ([#66](https://github.com/panel-extensions/panel-material-ui/pull/66))
- Align CI configuration ([#64](https://github.com/panel-extensions/panel-material-ui/pull/64))
- Bump pypa/gh-action-pypi-publish in the gh-actions group ([#52](https://github.com/panel-extensions/panel-material-ui/pull/52))
- Remove tests.util module ([#49](https://github.com/panel-extensions/panel-material-ui/pull/49))

### 🗂️ Other

- Standardize on primary color in theme ([#267](https://github.com/panel-extensions/panel-material-ui/pull/267))
- Assorted fixes ([#262](https://github.com/panel-extensions/panel-material-ui/pull/262))
- Make Page.template configurable ([#261](https://github.com/panel-extensions/panel-material-ui/pull/261))
- Treat Page.main as flex container ([#260](https://github.com/panel-extensions/panel-material-ui/pull/260))
- Reimplement editable sliders in React ([#258](https://github.com/panel-extensions/panel-material-ui/pull/258))
- Make theming robust to failed view lookups ([#251](https://github.com/panel-extensions/panel-material-ui/pull/251))
- Minor fixes for DiscreteSlider ([#240](https://github.com/panel-extensions/panel-material-ui/pull/240))
- Remove dotted border from bokeh plots ([#238](https://github.com/panel-extensions/panel-material-ui/pull/238))
- Toggle dark theme from query parameter ([#211](https://github.com/panel-extensions/panel-material-ui/pull/211))
- Automatically jslink widget references ([#206](https://github.com/panel-extensions/panel-material-ui/pull/206))
- Define exports of slider module ([#205](https://github.com/panel-extensions/panel-material-ui/pull/205))
- Font handling ([#202](https://github.com/panel-extensions/panel-material-ui/pull/202))
- Style tooltips ([#201](https://github.com/panel-extensions/panel-material-ui/pull/201))
- Automatically set bokeh theme client side ([#200](https://github.com/panel-extensions/panel-material-ui/pull/200))
- More layout fixes ([#198](https://github.com/panel-extensions/panel-material-ui/pull/198))
- Do no export all contents of notification module ([#186](https://github.com/panel-extensions/panel-material-ui/pull/186))
- Page theming fixes ([#183](https://github.com/panel-extensions/panel-material-ui/pull/183))
- Attempt to make test_notifications_destroy passed on Windows ([#157](https://github.com/panel-extensions/panel-material-ui/pull/157))
- Remove DateRangePicker and DatetimeRangePicker ([#136](https://github.com/panel-extensions/panel-material-ui/pull/136))
- Use image to render SVG icons ([#123](https://github.com/panel-extensions/panel-material-ui/pull/123))
- A range of small fixes ([#121](https://github.com/panel-extensions/panel-material-ui/pull/121))
- More SVG fixes ([#120](https://github.com/panel-extensions/panel-material-ui/pull/120))
- misc changes ([#119](https://github.com/panel-extensions/panel-material-ui/pull/119))
- Various fixes ([#106](https://github.com/panel-extensions/panel-material-ui/pull/106))
- Override ChatMessage background-color ([#104](https://github.com/panel-extensions/panel-material-ui/pull/104))
- Reimplement NumberInput widgets ([#95](https://github.com/panel-extensions/panel-material-ui/pull/95))
- TextArea sizing fixes and submit on shift+enter ([#96](https://github.com/panel-extensions/panel-material-ui/pull/96))
- Various minor widget fixes ([#85](https://github.com/panel-extensions/panel-material-ui/pull/85))
