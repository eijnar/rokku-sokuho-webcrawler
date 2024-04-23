import React, { useContext, useEffect, useRef } from 'react';
import { BandContext } from '../../contexts/BandContext';
import './BandCard.css';

const BandCard = ({ bandId }) => {
    const { bands, urls, fetchUrlsForBand } = useContext(BandContext);
    const cardRef = useRef(null);

    useEffect(() => {
        const cardElement = cardRef.current;
        const observer = new IntersectionObserver(entries => {

            entries.forEach(entry => {
                if (entry.isIntersecting && !urls[bandId]) {
                    fetchUrlsForBand(bandId);
                }
            });
        }, {
            rootMargin: '0px',
            threshold: 0.1
        });

        if (cardElement) {
            observer.observe(cardElement);
        }

        return () => {
            if (cardElement) {
                observer.unobserve(cardElement);
            }
        };
    }, [bandId, urls, fetchUrlsForBand]);

    const band = bands.find(b => b.band_id === parseInt(bandId, 10));
    const bandUrls = urls[bandId] || [];

    return (
        <div ref={cardRef} className="band-card">
            <div className="band-card-title">
                {band?.band_name}
            </div>
            <div className="band-card-body">
                <div className="band-card-details">
                    {bandUrls.map(url => (
                        <li key={url.url_id}>
                            <a href={url.url} target="_blank" rel="noopener noreferrer">{url.url}</a>
                        </li>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default BandCard;
