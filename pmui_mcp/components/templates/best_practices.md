# Panel Material UI - Best Practices

## General Guidelines

- Always import as `import panel_material_ui as pmui`.
- Always wrap your application in a `pmui.Page` component unless explicitly asked not to.
- For grid based layouts always use Grid or Flex layout components unless explicitly asked not to.
- Don't use aliases (e.g. `name`, `button_type` etc) for components unless explicitly asked to do so. Use the new names (e.g. `label`, `color`) instead.
- Use `sizing_mode` mode parameters over `sx` css styling parameter.
- Use Material UI `sx` parameter for all css styling of components except `sizing_mode`.
- Note that the `Page.sidebar` is 300px wide by default and thus widgets and other components should be laid out vertically.
- Note that the `Page.header` is 100px high by default and thus we should not put advanced widgets like Alerts into it. Normally only buttons, indicators, text and links go into the header.
- In the `Page.sidebar` the order should be 1) optional image 2) optional, short app title + description 3) input widgets, filters etc 4) additional documentation
- Make sure elements in the `Page.sidebar` stretch to the available width
- Don't include extra ThemeToggle component when using `Page`. Its already built in.

## Does and Don'ts

DON'T use `xs` parameter - it does not exist. DO user `size` parameter instead.

### List like layouts

For list-like layouts like `Column` and `Row` DON'T provide children in a list

```python
pmui.Row([child1, child2, child3,])
```

Instead DO provide them as separate arguments:

```python
pmui.Row(child1, child2, child3)
```

### Page titles, descriptions and widgets

When using the `Page` component DON'T:

- Provide the title, description or widgets in the `main` component

instead DO:

- Provide the title as the `Page.title` argument
- Provide the description as a child to the `Page.sidebar` argument
- Provide the widgets as children to the `Page.sidebar` argument

### sidebar, main and header elements

DON'T provide non-lists as children to the `Page.sidebar`, `Page.main` or `Page.header` arguments:

```python
pmui.Page(
    header=component1,  # This is incorrect
    sidebar=component2,  # This is incorrect
    main=component3,  # This is incorrect
)
```

DO provide lists of children to the `Page.sidebar`, `Page.main` or `Page.header` arguments:

```python
pmui.Page(
    header=[component1, component2],  # This is correct
    sidebar=[component3, component4],  # This is correct
    main=[component5, component6],  # This is correct
)
```
