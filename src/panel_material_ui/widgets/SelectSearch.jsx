import {useState} from 'react';
import InputAdornment from '@mui/material/InputAdornment';
import FilterListIcon from '@mui/icons-material/FilterList';
import ClearIcon from '@mui/icons-material/Clear';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import MenuItem from '@mui/material/MenuItem';
import ListItemText from '@mui/material/ListItemText';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import Select from '@mui/material/Select';
import OutlinedInput from '@mui/material/OutlinedInput';

export function render({ model, el }) {
    const [options] = model.useState("options");
    const [optionsLabels] = model.useState("options_labels");
    const [bookmarks] = model.useState("bookmarks");
    const [value, setValue] = model.useState("value");
    const [filterStr, setFilterStr] = model.useState("filter_str");
    const [placeholder] = model.useState("placeholder");
    const [title] = model.useState("title");

    const [width] = model.useState("width");
    const [dropdownHeight] = model.useState("dropdown_height");
    
    const [anchorPosition, setAnchorPosition] = useState({ top: 500, left: 50 });

    const [open, setOpen] = model.useState("dropdown_open"); // Explicitly track dropdown state

    const selectDidOpen = (event) => {

        const elRect = el.getBoundingClientRect();
        const parentRect = document.getElementsByTagName("fast-card")[0]?.getBoundingClientRect() || { top: 0, left: 0 };
        setAnchorPosition({
            top: elRect.bottom - parentRect.top,
            left: elRect.left - parentRect.left
        });

        setOpen(true);
    };

    const handleSearchChange = (event) => {
        setFilterStr(event.target.value);
        event.stopPropagation();
    };

    const closeDropdown = () => {
        setOpen(false);
        setFilterStr("");
    }

    const handleClickOnOption = (opt) => {
        setValue(opt);
        closeDropdown();
    };

    const bookmarkedOptions = bookmarks
        .map(opt => ({ value: opt, label: optionsLabels ? optionsLabels[options.indexOf(opt)] : opt }))
        .filter(({ label }) => label.toLowerCase().includes(filterStr.toLowerCase()));

    const filteredOptions = options
        .map((opt, index) => ({ value: opt, label: optionsLabels ? optionsLabels[index] : opt }))
        .filter(({ label }) => label.toLowerCase().includes(filterStr.toLowerCase()))
        .filter(({ value }) => !bookmarks.includes(value));

        

    const getLabelForValue = (val) => {
        const index = options.indexOf(val);
        return optionsLabels && optionsLabels[index] ? optionsLabels[index] : val;
    };

    const MenuProps = {
        container: el,
        anchorReference: "anchorPosition",
        anchorPosition: anchorPosition,
        PaperProps: {
            style: {
                width: width,
                height: dropdownHeight,
            },
            sx: {
                "& .MuiList-root": { paddingTop: 0, paddingBottom: 0 },
                top: 0,
                left: 0,
                //backgroundColor:"rgba(255,0,0,64)", // debug
            },
        },
        transformOrigin: "0px 0px",
        sx: {
            // backgroundColor:"rgba(0,0,255,64)", // debug
        },
        onClick: (e) => { if (e.target.type !== 'text'){ closeDropdown(); }  },
    };

    return (
        <FormControl variant="outlined">
            <InputLabel shrink sx={{translate:"15px 15px"}}>{title}</InputLabel>
            <Select
                variant="outlined"
                value={value}
                input={<OutlinedInput notched label={title} />}
                displayEmpty
                MenuProps={MenuProps}
                open={open}
                onOpen={() => {selectDidOpen();}  }
                renderValue={(selected) => selected ? getLabelForValue(selected) : placeholder}
                sx={{   padding: 0, 
                        margin:0, 
                        width:width,
                }}
            >
                <MenuItem disableGutters 
                    sx={{ paddingTop:0, paddingBottom:0, }}>
                    <TextField
                        sx={{ paddingTop: 0, paddingBottom: 0, width:1 }}
                        variant="filled"
                        placeholder="Search..."
                        value={filterStr}
                        onChange={handleSearchChange}
                        onFocus={(e) => {e.stopPropagation();}}
                        slotProps={{
                            input: {
                                startAdornment: (
                                    <InputAdornment position="start">
                                        <FilterListIcon />
                                    </InputAdornment>
                                ),
                                endAdornment: (
                                    <InputAdornment position="end">
                                        <ClearIcon onClick={()=>{setFilterStr("")}}/>
                                    </InputAdornment>
                                ),
                            },
                        }}
                    />
                </MenuItem>

                <Box sx={{ overflowY: "auto", 
                            height: dropdownHeight - 54*2,
                                marginLeft:2 }}>
                {bookmarkedOptions.length > 0 && (
                    <>
                        {bookmarkedOptions.map(({ value: opt, label }) => (
                            <MenuItem key={opt} value={opt} disableGutters 
                                onClick={(e) => {
                                    handleClickOnOption(opt);
                                }}
                            >
                                <ListItemText primary={label} />
                            </MenuItem>
                        ))}
                        <MenuItem disabled divider />
                    </>
                )}
                
                    {filteredOptions.map(({ value: opt, label }) => (
                        <MenuItem key={opt} value={opt} disableGutters 
                            onClick={(e) => {
                                handleClickOnOption(opt);
                            }}
                        >
                            <ListItemText primary={label} />
                        </MenuItem>
                    ))}
                </Box>
            </Select>
        </FormControl>
    );
}