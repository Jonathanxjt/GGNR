import React, { useState } from 'react';
import { Form, Button } from 'react-bootstrap';

const CreateEvent = () => {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [date, setDate] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        // Handle form submission logic here
    };

    return (
        <div className='container'>
            <Form onSubmit={handleSubmit}>
            <Form.Group controlId="title">
                <Form.Label>Title</Form.Label>
                <Form.Control
                    type="text"
                    placeholder="Enter title"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                />
            </Form.Group>

            <Form.Group controlId="description">
                <Form.Label>Description</Form.Label>
                <Form.Control
                    as="textarea"
                    rows={3}
                    placeholder="Enter description"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                />
            </Form.Group>

            <Form.Group controlId="date">
                <Form.Label>Date</Form.Label>
                <Form.Control
                    type="date"
                    placeholder="Enter date"
                    value={date}
                    onChange={(e) => setDate(e.target.value)}
                />
            </Form.Group>

            <Button variant="primary" type="submit">
                Create Event
            </Button>
        </Form>

        </div>
    );
};

export default CreateEvent;