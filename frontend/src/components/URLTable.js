import React, { useState } from 'react';
import axios from 'axios';
import { FaEdit, FaTrash, FaSave, FaTimes, FaPlus } from 'react-icons/fa'; // Import FontAwesome icons



const URLTable = ({ urls, bandId, onRemoveUrl, onEditUrl, fetchBands }) => {
    const [editUrlId, setEditUrlId] = useState(null);
    const [newUrl, setNewUrl] = useState({ url: '', class_name: '' });
    const [editingUrl, setEditingUrl] = useState({ url: '', class_name: '' });

    const getStatusClass = (url) => {
        // Check if there are valid date strings and create Date objects if they exist
        const lastUpdated = url.last_updated ? new Date(url.last_updated) : null;
        const lastFailed = url.last_failed ? new Date(url.last_failed) : null;

        // Determine the status class based on date comparison
        // Default to 'table-status-ok' if there is no last_failed date
        if (!lastFailed || (lastUpdated && lastUpdated > lastFailed)) {
            return "table-status-ok";  // OK status if never failed or updated after last fail
        } else {
            return "table-status-fail";    // Fail status if failed after last update or no updates at all
        }
    };

    const [isAddingUrl, setIsAddingUrl] = useState(false);

    const handleAddClick = () => {
        setIsAddingUrl(true);
    };
    const handleCancelNewUrl = () => {
        setNewUrl({ url: '', class_name: '' });  // Reset the input fields
        setIsAddingUrl(false);  // Hide the input fields and show the "Add URL" button again
    };

    // Example onSaveUrl function in Band.js
    const saveNewUrl = async (bandId, urlData) => {
        try {
            const response = await axios.post(`http://localhost:8000/urls`, {
                band_id: bandId,
                ...urlData
            });
            fetchBands();  // Assuming fetchBands refreshes the data from the server
        } catch (error) {
            console.error("Failed to save new URL:", error);
        }
    }

    const handleEdit = (url) => {
        setEditUrlId(url.url_id);
        setEditingUrl({ ...url });
    };

    const handleSaveEdit = (urlId) => {
        onEditUrl(urlId, editingUrl);
        setEditUrlId(null);
    };

    const handleCancelEdit = () => {
        setEditUrlId(null);
    };

    const handleSaveNewUrl = () => {
        saveNewUrl(bandId, newUrl);  // Your existing function to save the new URL
        setNewUrl({ url: '', class_name: '' });  // Reset the input fields after saving
        setIsAddingUrl(false);  // Hide the input fields and show the Add button again
    };

    return (
        <table className="table-full-width">
            <thead>
                <tr>
                    <th className="table-header">Status</th>
                    <th className="table-header">URL</th>
                    <th className="table-header">Class Name</th>
                    <th className="table-header">Actions</th>
                </tr>
            </thead>
            <tbody>
                {urls.map((url) => (
                    <tr key={url.url_id} className="table-striped-row">
                        <td className="table-cell table-status">
                            <span className={`table-status-dot ${getStatusClass(url)}`}></span>
                        </td>
                        <td className="table-cell">
                            {editUrlId === url.url_id ? (
                                <input type="text" value={editingUrl.url} onChange={(e) => setEditingUrl({ ...editingUrl, url: e.target.value })} className="table-input" />
                            ) : (
                                url.url
                            )}
                        </td>
                        <td className="table-cell">
                            {editUrlId === url.url_id ? (
                                <input type="text" value={editingUrl.class_name} onChange={(e) => setEditingUrl({ ...editingUrl, class_name: e.target.value })} className="table-input" />
                            ) : (
                                url.class_name
                            )}
                        </td>
                        <td className="table-cell table-action-buttons">
                            <div className="action-buttons">
                                {editUrlId === url.url_id ? (
                                    <>
                                        <button onClick={() => handleSaveEdit(url.url_id)} className="icon-button save-button"><FaSave /></button>
                                        <button onClick={handleCancelEdit} className="icon-button cancel-button"><FaTimes /></button>
                                    </>
                                ) : (
                                    <>
                                        <button onClick={() => handleEdit(url)} className="icon-button edit-button"><FaEdit /></button>
                                        <button onClick={() => onRemoveUrl(url.url_id)} className="icon-button delete-button"><FaTrash /></button>
                                    </>
                                )}
                            </div>
                        </td>
                    </tr>
                ))}
    {isAddingUrl ? (
        <tr>
            <td className="table-cell"></td>  {/* First column remains empty */}
            <td className="table-cell">
                <input type="text" placeholder="Enter URL" className="table-input" value={newUrl.url} onChange={(e) => setNewUrl({ ...newUrl, url: e.target.value })} />
            </td>
            <td className="table-cell">
                <input type="text" placeholder="Enter Class Name" className="table-input" value={newUrl.class_name} onChange={(e) => setNewUrl({ ...newUrl, class_name: e.target.value })} />
            </td>
            <td className="table-cell">
                <button onClick={handleSaveNewUrl} className="icon-button save-button"><FaSave /></button>
                <button onClick={handleCancelNewUrl} className="icon-button cancel-button"><FaTimes /></button>
            </td>
        </tr>
    ) : (
        <tr>
            <td className="table-cell"><button onClick={handleAddClick} className="icon-button"><FaPlus /></button></td>
            <td className="table-cell"></td>
            <td className="table-cell"></td>
            <td className="table-cell"></td>
        </tr>
    )}
            </tbody>
        </table>
    );
};

export default URLTable;
