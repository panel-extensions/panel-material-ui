import {useState} from 'react';
import InputAdornment from '@mui/material/InputAdornment';
import FilterListIcon from '@mui/icons-material/FilterList';
import ClearIcon from '@mui/icons-material/Clear';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import MenuItem from '@mui/material/MenuItem';
import Checkbox from '@mui/material/Checkbox';
import ListItemText from '@mui/material/ListItemText';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import Select from '@mui/material/Select';
import OutlinedInput from '@mui/material/OutlinedInput';

export function render({ model, el }) {
    
    const [title] = model.useState("title");
    const [label] = model.useState("label");
    const [options] = model.useState("options");
    const [optionsLabels] = model.useState("options_labels");
    const [value, setValue] = model.useState("value");
    const [filterStr, setFilterStr] = model.useState("filter_str");
    
    const [width] = model.useState("width");
    const [dropdownHeight] = model.useState("dropdown_height");
    
    // Store anchorPosition in state to trigger re-renders
    const [anchorPosition, setAnchorPosition] = useState({ top: 500, left: 50 });

    const handleClick = (event) => {
        const elRect = el.getBoundingClientRect();
        const parentRect = document.getElementsByTagName("fast-card")[0]?.getBoundingClientRect() || { top: 0, left: 0 };

        const res = {
            top: elRect.bottom - parentRect.top,
            left: elRect.left - parentRect.left
        }

        setAnchorPosition(res);
    };

    const handleSearchChange = (event) => {
        setFilterStr(event.target.value);
    };
    
    const filteredIndices = options
        .map((opt, index) => ({ value: opt, label: optionsLabels === null ? opt : optionsLabels[index], index }))
        .filter(({ label }) => label.toLowerCase().includes(filterStr.toLowerCase()));

    const allSelected = value.length === options.length;

    const handleSelectAllChange = (event) => {
        
        if (event.target.checked) {
            setValue([...options]);  // Select all options
        } else {
            setValue([]);  // Deselect all
        }
    };

    const MenuProps = {
        container: el,
        anchorReference: "anchorPosition",
        anchorPosition:anchorPosition,
        PaperProps: {
            style: {
                width: width,
                height: dropdownHeight,
            },
            sx:{
                // Necessary to play nice with FastListTemplate,
                // Might not be necessary otherwise
                "& .MuiList-root": { paddingTop: 0,
                    paddingBottom: 0,
                },
                top: 0,
                left: 0,
                //backgroundColor:"#FF7F5077", // debug
                
            },
            
        },
        transformOrigin: "0px 0px",
        sx: {
            //backgroundColor:"#7FFFD477", // debug
            },
        
        
    };

    const get_select_all_label = () => {
        if ( filterStr.length == 0){
            return "Select All";
        } else {
            return filteredIndices.length + " filtered results";
        }
    }
    
    return (
        <FormControl variant="outlined">
        <InputLabel shrink sx={{translate:"15px 15px"}}>{title}</InputLabel>
        <Select
            multiple
            variant="outlined"
            label={title}
            value={value}
            input={<OutlinedInput label={title} notched />}
            renderValue={(selected) => label}
            displayEmpty
            MenuProps={MenuProps}
            sx={{ padding: 0, 
                  margin:0, 
                  width:width,
            }}
            onOpen={handleClick}
            
        >

            <MenuItem disableGutters="true" 
                sx={{ paddingTop:0, paddingBottom:0, }}
            >
                <TextField
                    sx={{ paddingTop: 0, paddingBottom: 0, width:1 }}
                    variant="filled"
                    placeholder="Search..."
                    value={filterStr}
                    onChange={handleSearchChange}

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
            
            <MenuItem disableGutters="true" divider="true">  
                
                <Checkbox   
                    checked={value.length === options.length}
                    indeterminate={value.length > 0 && value.length < options.length}
                    onClick={(e) => {
                        console.log(e);
                        setValue(value.length === options.length ? [] : [...options]);
                    }}
                />
               
                <ListItemText primary={get_select_all_label()} />


            </MenuItem>

            <Box sx={{ overflowY: "auto", height: dropdownHeight - 54*2 }}>
            {filteredIndices.map(({ value: opt, label }) => (
                <MenuItem key={opt} value={opt} disableGutters="true">
                    <Checkbox checked={value.includes(opt)}
                    onClick={(e) => {
                        const isChecked = !value.includes(opt); // Manually determine checked state, because bugs.

                        if (isChecked) {
                            setValue([...value, opt]); // Add selection
                        } else {
                            setValue(value.filter(v => v !== opt)); // Remove selection
                        }
                    }}
                    />
                    <ListItemText primary={label}  />
                </MenuItem>
            ))}
            </Box>

        </Select>
        </FormControl>
    );

}
