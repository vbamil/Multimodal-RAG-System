// File: src/components/TablesView.js

import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { Typography, Accordion, AccordionSummary, AccordionDetails, Box, Select, MenuItem, FormControl, InputLabel, Table as MuiTable, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import NavigationButtons from './NavigationButtons';
import './TablesView.css';

const TablesView = ({ tables, onBack }) => {
    const [selectedMethod, setSelectedMethod] = useState(Object.keys(tables)[0] || '');

    const handleChange = (event) => {
        setSelectedMethod(event.target.value);
    };

    return (
        <Box sx={{ mt: 4, mb: 4 }}>
            {/* Top Navigation Buttons */}
            <NavigationButtons onBack={onBack} onNext={() => {}} showNext={false} />

            <Typography variant="h5" gutterBottom>
                📋 Extracted Tables
            </Typography>

            {/* Method Selector */}
            <FormControl fullWidth sx={{ mb: 3 }}>
                <InputLabel id="table-method-select-label">Select Table Extraction Method</InputLabel>
                <Select
                    labelId="table-method-select-label"
                    id="table-method-select"
                    value={selectedMethod}
                    label="Select Table Extraction Method"
                    onChange={handleChange}
                >
                    {Object.keys(tables).length > 0 ? (
                        Object.keys(tables).map((method) => (
                            <MenuItem key={method} value={method}>
                                {method}
                            </MenuItem>
                        ))
                    ) : (
                        <MenuItem value="">No Table Extraction Methods Available</MenuItem>
                    )}
                </Select>
            </FormControl>

            {/* Display Tables */}
            {selectedMethod && tables[selectedMethod] && tables[selectedMethod].length > 0 ? (
                tables[selectedMethod].map((table, index) => (
                    <Accordion key={index}>
                        <AccordionSummary
                            expandIcon={<ExpandMoreIcon />}
                            aria-controls={`table-panel-${index}-content`}
                            id={`table-panel-${index}-header`}
                        >
                            <Typography>🗃️ {selectedMethod} - Table {table.table_number} {table.page_number ? `(Page ${table.page_number})` : ''}</Typography>
                        </AccordionSummary>
                        <AccordionDetails>
                            <TableContainer component={Paper}>
                                <MuiTable aria-label="extracted table">
                                    <TableHead>
                                        <TableRow>
                                            {table.rows[0].cells.map((cell, idx) => (
                                                <TableCell key={idx}>{cell || `Header ${idx + 1}`}</TableCell>
                                            ))}
                                        </TableRow>
                                    </TableHead>
                                    <TableBody>
                                        {table.rows.slice(1).map((row, rowIndex) => (
                                            <TableRow key={rowIndex}>
                                                {row.cells.map((cell, cellIndex) => (
                                                    <TableCell key={cellIndex}>{cell}</TableCell>
                                                ))}
                                            </TableRow>
                                        ))}
                                    </TableBody>
                                </MuiTable>
                            </TableContainer>
                        </AccordionDetails>
                    </Accordion>
                ))
            ) : (
                <Typography>No tables available for the selected method.</Typography>
            )}

            {/* Bottom Navigation Buttons */}
            <NavigationButtons onBack={onBack} onNext={() => {}} showNext={false} />
        </Box>
    );
};

TablesView.propTypes = {
    tables: PropTypes.objectOf(
        PropTypes.arrayOf(
            PropTypes.shape({
                page_number: PropTypes.number.isRequired,
                table_number: PropTypes.number.isRequired,
                rows: PropTypes.arrayOf(
                    PropTypes.shape({
                        cells: PropTypes.arrayOf(PropTypes.string).isRequired,
                    })
                ).isRequired,
            })
        )
    ).isRequired,
    onBack: PropTypes.func.isRequired,
};

export default TablesView;
