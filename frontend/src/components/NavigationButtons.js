// File: src/components/NavigationButtons.js

import React from 'react';
import PropTypes from 'prop-types';
import { Button, Box } from '@mui/material';

const NavigationButtons = ({ onBack, onNext, showNext = true, showBack = true }) => {
    return (
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 2, mb: 2 }}>
            {showBack ? (
                <Button variant="contained" color="inherit" onClick={onBack}>
                    ← Back
                </Button>
            ) : (
                <Box />
            )}
            {showNext ? (
                <Button variant="contained" color="primary" onClick={onNext}>
                    Next →
                </Button>
            ) : (
                <Box />
            )}
        </Box>
    );
};

NavigationButtons.propTypes = {
    onBack: PropTypes.func,
    onNext: PropTypes.func,
    showNext: PropTypes.bool,
    showBack: PropTypes.bool,
};

NavigationButtons.defaultProps = {
    onBack: () => {},
    onNext: () => {},
    showNext: true,
    showBack: true,
};

export default NavigationButtons;
