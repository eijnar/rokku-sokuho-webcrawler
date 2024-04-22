import React from 'react';
import axios from 'axios';
import { FaTrash } from 'react-icons/fa';
import URLTable from './URLTable';
import './styles/BandManager.css';

const Band = ({ band, fetchBands }) => {
    const handleDeleteBand = async () => {
        try {
            await axios.delete(`http://localhost:8000/bands/${band.band_id}`);
            fetchBands();  // Refresh the list of bands
        } catch (error) {
            console.error("Failed to delete band:", error);
        }
    };

    const handleRemoveUrl = async (urlId) => {
        try {
            await axios.delete(`http://localhost:8000/urls/${urlId}`);
            // Refresh the list of URLs for the band after deletion
            fetchBands();
        } catch (error) {
            console.error("Failed to delete URL:", error);
        }
    };

    const handleEditUrl = async (urlId, updatedUrlInfo) => {
        try {
            await axios.put(`http://localhost:8000/urls/${urlId}`, updatedUrlInfo);
            // Refresh the list of URLs for the band after update
            fetchBands();
        } catch (error) {
            console.error("Failed to update URL:", error);
        }
    };

    return (
        <div className="band-container">
            <div className="band-details">
                <h2>{band.band_name}</h2>
                <button onClick={handleDeleteBand} className="band-delete-button">
                    <FaTrash />
                </button>
            </div>
            <div className="band-actions">
            <URLTable
    urls={band.urls || []}
    bandId={band.band_id}
    onRemoveUrl={handleRemoveUrl}
    onEditUrl={handleEditUrl}
    fetchBands={fetchBands}
/>

            </div>
        </div>
    );
};

export default Band;
