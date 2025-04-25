import pnmui_bundle from "./panel-material-ui.bundle.js";
const ReactDOM = pnmui_bundle.react_dom

export default ReactDOM;
export const {
  createPortal,
  findDOMNode,
  flushSync,
  hydrate,
  render,
  unmountComponentAtNode
} = ReactDOM;
