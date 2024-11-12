// File: src/pages/HomePage.js

import React, { useState } from 'react';
import UploadForm from '../components/UploadForm';
import MetricsSummary from '../components/MetricsSummary';
import ChunksView from '../components/ChunksView';
import EntitiesView from '../components/EntitiesView';
import TablesView from '../components/TablesView';
import { Stepper, Step, StepLabel, Typography, Box } from '@mui/material';
import Joyride, { STATUS } from 'react-joyride'; // Ensure react-joyride is installed
import './HomePage.css';
import NavigationButtons from '../components/NavigationButtons'; // Ensure this is correctly imported

// Separate step arrays
const stepperSteps = [
    'Upload Document',
    'View Metrics Summary',
    'View Chunks',
    'View Entities',
    'View Tables',
];

const joyrideSteps = [
    {
        target: '.upload-form',
        content: 'Start by uploading your document here.',
    },
    {
        target: '.metrics-section',
        content: 'Here you can view the summary metrics of your document.',
    },
    {
        target: '.chunks-section',
        content: 'View the chunks of your document for detailed analysis.',
    },
    {
        target: '.entities-section',
        content: 'Explore the entities extracted from your document.',
    },
    {
        target: '.tables-section',
        content: 'Check out the tables extracted from your document.',
    },
];

const HomePage = () => {
    const [activeStep, setActiveStep] = useState(0);
    const [data, setData] = useState({
        chunking: {},
        metrics: null,
        entities: {},
        tables: {},
    });
    const [error, setError] = useState(null);
    const [runTour, setRunTour] = useState(true);

    const handleUploadSuccess = (responseData) => {
        // Select only the first available chunking method
        const chunkingMethods = Object.keys(responseData.chunking);
        const bestChunkingMethod = chunkingMethods.length > 0 ? chunkingMethods[0] : null;
        const bestChunkingData = bestChunkingMethod ? { [bestChunkingMethod]: responseData.chunking[bestChunkingMethod] } : {};

        setData({
            chunking: bestChunkingData,
            metrics: {
                num_lines: responseData.num_lines,
                num_paragraphs: responseData.num_paragraphs,
                num_words: responseData.num_words,
                avg_words_per_paragraph: responseData.avg_words_per_paragraph,
                avg_words_per_line: responseData.avg_words_per_line,
                original_content_size: responseData.original_content_size,
                num_chunks: responseData.num_chunks,
            },
            entities: responseData.entities || {},
            tables: responseData.tables || {},
        });
        setActiveStep((prev) => prev + 1);
    };

    const handleUploadError = (errorMessage) => {
        setError(errorMessage);
    };

    const handleNext = () => {
        setActiveStep((prev) => prev + 1);
    };

    const handleBack = () => {
        setActiveStep((prev) => prev - 1);
    };

    const handleJoyrideCallback = (data) => {
        const { status } = data;
        const finishedStatuses = [STATUS.FINISHED, STATUS.SKIPPED];

        if (finishedStatuses.includes(status)) {
            setRunTour(false);
        }
    };

    const getStepContent = (step) => {
        switch (step) {
            case 0:
                return <UploadForm onUploadSuccess={handleUploadSuccess} onUploadError={handleUploadError} />;
            case 1:
                return (
                    <MetricsSummary
                        metrics={data.metrics}
                        onNext={handleNext}
                        onBack={handleBack}
                    />
                );
            case 2:
                return (
                    <ChunksView
                        chunking={data.chunking}
                        onNext={handleNext}
                        onBack={handleBack}
                    />
                );
            case 3:
                return (
                    <EntitiesView
                        entities={data.entities}
                        onNext={handleNext}
                        onBack={handleBack}
                    />
                );
            case 4:
                return (
                    <TablesView
                        tables={data.tables}
                        onBack={handleBack}
                    />
                );
            default:
                return 'Unknown step';
        }
    };

    return (
        <div className="home-page">
            <Joyride
                steps={joyrideSteps}
                run={runTour}
                continuous
                showProgress
                showSkipButton
                callback={handleJoyrideCallback}
                styles={{
                    options: {
                        zIndex: 10000,
                    },
                }}
            />
            <Typography variant="h4" align="center" gutterBottom>
                📚 Multimodal Retrieval-Augmented Generation System
            </Typography>
            <Box sx={{ width: '80%', margin: '0 auto' }}>
                <Stepper activeStep={activeStep} alternativeLabel>
                    {stepperSteps.map((label, index) => (
                        <Step key={index}>
                            <StepLabel>{label}</StepLabel>
                        </Step>
                    ))}
                </Stepper>
                <div>
                    {activeStep === stepperSteps.length ? (
                        <Typography variant="h6" align="center" sx={{ mt: 4, mb: 2 }}>
                            🎉 All steps completed! Thank you for using the system.
                        </Typography>
                    ) : (
                        <div>
                            {error && (
                                <Typography variant="body1" color="error" align="center" sx={{ mt: 2 }}>
                                    ❌ Error: {error}
                                </Typography>
                            )}
                            {getStepContent(activeStep)}
                        </div>
                    )}
                </div>
            </Box>
        </div>
    );
};

export default HomePage;
