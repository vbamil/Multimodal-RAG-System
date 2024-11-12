// File: src/components/EntitiesView.js

import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { Typography, Accordion, AccordionSummary, AccordionDetails, Box, Select, MenuItem, FormControl, InputLabel } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import NavigationButtons from './NavigationButtons';
import './EntitiesView.css';

const EntitiesView = ({ entities, onNext, onBack }) => {
    const [selectedMethod, setSelectedMethod] = useState(Object.keys(entities)[0] || '');

    const handleChange = (event) => {
        setSelectedMethod(event.target.value);
    };

    return (
        <Box sx={{ mt: 4, mb: 4 }}>
            {/* Top Navigation Buttons */}
            <NavigationButtons onBack={onBack} onNext={onNext} showBack={false} />

            <Typography variant="h5" gutterBottom>
                🔍 Entity Extraction
            </Typography>

            {/* Method Selector */}
            <FormControl fullWidth sx={{ mb: 3 }}>
                <InputLabel id="entity-method-select-label">Select Entity Extraction Method</InputLabel>
                <Select
                    labelId="entity-method-select-label"
                    id="entity-method-select"
                    value={selectedMethod}
                    label="Select Entity Extraction Method"
                    onChange={handleChange}
                >
                    {Object.keys(entities).length > 0 ? (
                        Object.keys(entities).map((method) => (
                            <MenuItem key={method} value={method}>
                                {method}
                            </MenuItem>
                        ))
                    ) : (
                        <MenuItem value="">No Entity Extraction Methods Available</MenuItem>
                    )}
                </Select>
            </FormControl>

            {/* Display Entities */}
            {selectedMethod && entities[selectedMethod] && entities[selectedMethod].length > 0 ? (
                entities[selectedMethod].map((entityList, index) => (
                    <Accordion key={index}>
                        <AccordionSummary
                            expandIcon={<ExpandMoreIcon />}
                            aria-controls={`panel-${index}-content`}
                            id={`panel-${index}-header`}
                        >
                            <Typography>Chunk {index + 1}</Typography>
                        </AccordionSummary>
                        <AccordionDetails>
                            {entityList.length > 0 ? (
                                <ul>
                                    {entityList.map((entity, idx) => (
                                        <li key={idx}>
                                            <strong>{entity.text}</strong> ({entity.label})
                                        </li>
                                    ))}
                                </ul>
                            ) : (
                                <Typography>No entities found in this chunk.</Typography>
                            )}
                        </AccordionDetails>
                    </Accordion>
                ))
            ) : (
                <Typography>No entities available for the selected method.</Typography>
            )}

            {/* Bottom Navigation Buttons */}
            <NavigationButtons onBack={onBack} onNext={onNext} />
        </Box>
    );
};

EntitiesView.propTypes = {
    entities: PropTypes.objectOf(
        PropTypes.arrayOf(
            PropTypes.shape({
                text: PropTypes.string.isRequired,
                label: PropTypes.string.isRequired,
            })
        )
    ).isRequired,
    onNext: PropTypes.func.isRequired,
    onBack: PropTypes.func.isRequired,
};

export default EntitiesView;
