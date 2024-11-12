// File: src/components/MetricsSummary.js

import React from 'react';
import PropTypes from 'prop-types';
import { Typography, List, ListItem, ListItemText, Box } from '@mui/material';
import NavigationButtons from './NavigationButtons';
import './MetricsSummary.css';

const MetricsSummary = ({ metrics, onNext, onBack }) => {
    return (
        <Box sx={{ mt: 4, mb: 4 }}>
            {/* Top Navigation Buttons */}
            <NavigationButtons onBack={onBack} onNext={onNext} showBack={false} />

            <Typography variant="h5" gutterBottom>
                📊 Metrics Summary
            </Typography>
            <List>
                <ListItem>
                    <ListItemText primary="Number of Lines" secondary={metrics.num_lines} />
                </ListItem>
                <ListItem>
                    <ListItemText primary="Number of Paragraphs" secondary={metrics.num_paragraphs} />
                </ListItem>
                <ListItem>
                    <ListItemText primary="Number of Words" secondary={metrics.num_words} />
                </ListItem>
                <ListItem>
                    <ListItemText primary="Average Words per Paragraph" secondary={metrics.avg_words_per_paragraph.toFixed(2)} />
                </ListItem>
                <ListItem>
                    <ListItemText primary="Average Words per Line" secondary={metrics.avg_words_per_line.toFixed(2)} />
                </ListItem>
                <ListItem>
                    <ListItemText primary="Original Content Size" secondary={`${metrics.original_content_size} bytes`} />
                </ListItem>
                <ListItem>
                    <ListItemText primary="Number of Chunks" secondary={metrics.num_chunks} />
                </ListItem>
            </List>

            {/* Bottom Navigation Buttons */}
            <NavigationButtons onBack={onBack} onNext={onNext} />
        </Box>
    );
};

MetricsSummary.propTypes = {
    metrics: PropTypes.shape({
        num_lines: PropTypes.number.isRequired,
        num_paragraphs: PropTypes.number.isRequired,
        num_words: PropTypes.number.isRequired,
        avg_words_per_paragraph: PropTypes.number.isRequired,
        avg_words_per_line: PropTypes.number.isRequired,
        original_content_size: PropTypes.number.isRequired,
        num_chunks: PropTypes.number.isRequired,
    }).isRequired,
    onNext: PropTypes.func.isRequired,
    onBack: PropTypes.func.isRequired,
};

export default MetricsSummary;
