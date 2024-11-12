// File: src/components/ChunksView.js

import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { Typography, Accordion, AccordionSummary, AccordionDetails, Box } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import NavigationButtons from './NavigationButtons';
import './ChunksView.css';

const ChunksView = ({ chunking, onNext, onBack }) => {
    const [expanded, setExpanded] = useState(false);

    const handleChange = (panel) => (event, isExpanded) => {
        setExpanded(isExpanded ? panel : false);
    };

    // Since only one chunking method is present, extract it
    const chunkingMethod = Object.keys(chunking)[0];
    const chunks = chunking[chunkingMethod] || [];

    return (
        <Box sx={{ mt: 4, mb: 4 }}>
            {/* Top Navigation Buttons */}
            <NavigationButtons onBack={onBack} onNext={onNext} showBack={false} />

            <Typography variant="h5" gutterBottom>
                📄 Document Chunks ({chunkingMethod})
            </Typography>
            {chunks.length > 0 ? (
                chunks.map((chunk, index) => (
                    <Accordion
                        key={index}
                        expanded={expanded === `chunk-${index}`}
                        onChange={handleChange(`chunk-${index}`)}
                    >
                        <AccordionSummary
                            expandIcon={<ExpandMoreIcon />}
                            aria-controls={`panel-${index}-content`}
                            id={`panel-${index}-header`}
                        >
                            <Typography>Chunk {index + 1}</Typography>
                        </AccordionSummary>
                        <AccordionDetails>
                            <Typography>{chunk}</Typography>
                        </AccordionDetails>
                    </Accordion>
                ))
            ) : (
                <Typography>No chunks available.</Typography>
            )}

            {/* Bottom Navigation Buttons */}
            <NavigationButtons onBack={onBack} onNext={onNext} />
        </Box>
    );
};

ChunksView.propTypes = {
    chunking: PropTypes.objectOf(PropTypes.arrayOf(PropTypes.string)).isRequired,
    onNext: PropTypes.func.isRequired,
    onBack: PropTypes.func.isRequired,
};

export default ChunksView;
