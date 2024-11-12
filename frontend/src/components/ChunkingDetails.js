// File: src/components/ChunkingDetails.js

import React, { useState } from 'react';
import PropTypes from 'prop-types';
import './ChunkingDetails.css';

const ChunkingDetails = ({ chunking, metrics, entities, tables }) => {
    const [expandedChunks, setExpandedChunks] = useState({});
    const [expandedTables, setExpandedTables] = useState({});

    // State for selected methods
    const [selectedChunkMethod, setSelectedChunkMethod] = useState(Object.keys(chunking)[0] || '');
    const [selectedEntityMethod, setSelectedEntityMethod] = useState(Object.keys(entities)[0] || '');
    const [selectedTableMethod, setSelectedTableMethod] = useState(Object.keys(tables)[0] || '');

    const toggleChunk = (index) => {
        setExpandedChunks((prev) => ({
            ...prev,
            [index]: !prev[index],
        }));
    };

    const toggleTable = (index) => {
        setExpandedTables((prev) => ({
            ...prev,
            [index]: !prev[index],
        }));
    };

    // Get available methods
    const chunkMethods = Object.keys(chunking);
    const entityMethods = Object.keys(entities);
    const tableMethods = Object.keys(tables);

    return (
        <div className="chunking-details">
            {/* Metrics Section */}
            <div className="metrics-section">
                <h3>📊 Metrics</h3>
                <ul>
                    <li><strong>Number of Lines:</strong> {metrics.num_lines}</li>
                    <li><strong>Number of Paragraphs:</strong> {metrics.num_paragraphs}</li>
                    <li><strong>Number of Words:</strong> {metrics.num_words}</li>
                    <li><strong>Average Words per Paragraph:</strong> {metrics.avg_words_per_paragraph}</li>
                    <li><strong>Average Words per Line:</strong> {metrics.avg_words_per_line}</li>
                    <li><strong>Original Content Size:</strong> {metrics.original_content_size} bytes</li>
                    <li><strong>Number of Chunks:</strong> {metrics.num_chunks}</li>
                </ul>
            </div>

            {/* Chunking Section */}
            <div className="chunks-section">
                <h3>📄 Chunks and Entities</h3>

                {/* Method Selector */}
                <div className="method-selector">
                    <label htmlFor="chunk-method-select">Select Chunking Method:</label>
                    <select
                        id="chunk-method-select"
                        value={selectedChunkMethod}
                        onChange={(e) => setSelectedChunkMethod(e.target.value)}
                    >
                        {chunkMethods.length > 0 ? (
                            chunkMethods.map((method) => (
                                <option key={method} value={method}>
                                    {method}
                                </option>
                            ))
                        ) : (
                            <option value="">No Chunking Methods Available</option>
                        )}
                    </select>
                </div>

                {/* Display Chunks */}
                {selectedChunkMethod && chunking[selectedChunkMethod] && chunking[selectedChunkMethod].length > 0 ? (
                    chunking[selectedChunkMethod].map((chunk, index) => (
                        <div key={index} className="chunk">
                            <div
                                className="chunk-header"
                                onClick={() => toggleChunk(index)}
                            >
                                <h4>📌 {selectedChunkMethod} - Chunk {index + 1}</h4>
                                <span>{expandedChunks[index] ? '▲' : '▼'}</span>
                            </div>
                            {expandedChunks[index] && (
                                <div className="chunk-content">
                                    <p>{chunk}</p>
                                    {entities[selectedEntityMethod] && entities[selectedEntityMethod][index] && entities[selectedEntityMethod][index].length > 0 && (
                                        <div className="entities-section">
                                            <h5>🔍 Entities ({selectedEntityMethod})</h5>
                                            <ul>
                                                {entities[selectedEntityMethod][index].map((entity, idx) => (
                                                    <li key={idx}>
                                                        <strong>{entity.text}</strong> ({entity.label})
                                                    </li>
                                                ))}
                                            </ul>
                                        </div>
                                    )}
                                </div>
                            )}
                        </div>
                    ))
                ) : (
                    <p>No chunks available for the selected method.</p>
                )}
            </div>

            {/* Entity Extraction Section */}
            <div className="entities-section">
                <h3>🔍 Entity Extraction</h3>

                {/* Method Selector */}
                <div className="method-selector">
                    <label htmlFor="entity-method-select">Select Entity Extraction Method:</label>
                    <select
                        id="entity-method-select"
                        value={selectedEntityMethod}
                        onChange={(e) => setSelectedEntityMethod(e.target.value)}
                    >
                        {entityMethods.length > 0 ? (
                            entityMethods.map((method) => (
                                <option key={method} value={method}>
                                    {method}
                                </option>
                            ))
                        ) : (
                            <option value="">No Entity Extraction Methods Available</option>
                        )}
                    </select>
                </div>

                {/* Display Entities */}
                {selectedEntityMethod && entities[selectedEntityMethod] && entities[selectedEntityMethod].length > 0 ? (
                    entities[selectedEntityMethod].map((entityList, index) => (
                        <div key={index} className="entity-list">
                            <h4>📌 Chunk {index + 1}</h4>
                            {entityList.length > 0 ? (
                                <ul>
                                    {entityList.map((entity, idx) => (
                                        <li key={idx}>
                                            <strong>{entity.text}</strong> ({entity.label})
                                        </li>
                                    ))}
                                </ul>
                            ) : (
                                <p>No entities found in this chunk.</p>
                            )}
                        </div>
                    ))
                ) : (
                    <p>No entities available for the selected method.</p>
                )}
            </div>

            {/* Tables Section */}
            <div className="tables-section">
                <h3>📋 Extracted Tables</h3>

                {/* Method Selector */}
                <div className="method-selector">
                    <label htmlFor="table-method-select">Select Table Extraction Method:</label>
                    <select
                        id="table-method-select"
                        value={selectedTableMethod}
                        onChange={(e) => setSelectedTableMethod(e.target.value)}
                    >
                        {tableMethods.length > 0 ? (
                            tableMethods.map((method) => (
                                <option key={method} value={method}>
                                    {method}
                                </option>
                            ))
                        ) : (
                            <option value="">No Table Extraction Methods Available</option>
                        )}
                    </select>
                </div>

                {/* Display Tables */}
                {selectedTableMethod && tables[selectedTableMethod] && tables[selectedTableMethod].length > 0 ? (
                    tables[selectedTableMethod].map((table, index) => (
                        <div key={index} className="table-container">
                            <div
                                className="table-header"
                                onClick={() => toggleTable(index)}
                            >
                                <h4>🗃️ {selectedTableMethod} - Table {index + 1} {table.page_number ? `(Page ${table.page_number})` : ''}</h4>
                                <span>{expandedTables[index] ? '▲' : '▼'}</span>
                            </div>
                            {expandedTables[index] && (
                                <div className="table-content">
                                    <table>
                                        <thead>
                                            <tr>
                                                {table.rows[0].cells.map((cell, idx) => (
                                                    <th key={idx}>{cell || `Header ${idx + 1}`}</th>
                                                ))}
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {table.rows.slice(1).map((row, rowIndex) => (
                                                <tr key={rowIndex}>
                                                    {row.cells.map((cell, cellIndex) => (
                                                        <td key={cellIndex}>{cell}</td>
                                                    ))}
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            )}
                        </div>
                    ))
                ) : (
                    <p>No tables available for the selected method.</p>
                )}
            </div>
        </div>
    );

};

    ChunkingDetails.propTypes = {
        chunking: PropTypes.objectOf(PropTypes.arrayOf(PropTypes.string)).isRequired,
        metrics: PropTypes.shape({
            num_lines: PropTypes.number.isRequired,
            num_paragraphs: PropTypes.number.isRequired,
            num_words: PropTypes.number.isRequired,
            avg_words_per_paragraph: PropTypes.number.isRequired,
            avg_words_per_line: PropTypes.number.isRequired,
            original_content_size: PropTypes.number.isRequired,
            num_chunks: PropTypes.number.isRequired,
        }).isRequired,
        entities: PropTypes.objectOf(
            PropTypes.arrayOf(
                PropTypes.shape({
                    text: PropTypes.string.isRequired,
                    label: PropTypes.string.isRequired,
                })
            )
        ).isRequired,
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
    };

    export default ChunkingDetails;
