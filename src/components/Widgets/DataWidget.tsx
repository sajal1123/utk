import { useState } from "react";
import { Button, Col, Collapse, Form, Row } from "react-bootstrap";
import { BiData } from "react-icons/bi";


type dataWidgetProps = {
    onCityRefChange: any
}

export function DataWidget({onCityRefChange}:dataWidgetProps) {
    const [dataOpen, setdataOpen] = useState(false)   

    return (<Row>
            <Col>
                    {
                    /* button for data, clicking on it will open the list of data */
                    }
                    <Button id="space" variant="outline-secondary" onClick={() => setdataOpen(!dataOpen)} aria-controls="example-collapse-text" aria-expanded={dataOpen}>
                            <BiData /> Data
                    </Button>

                    {
                    /* list of cities */
                    }
                    <Collapse in={dataOpen}>
                        <Form>
                            <Form.Group className="mb-3" controlId="formBasicCheckbox" id="space">
                                <Form.Check 
                                    type="radio" 
                                    label="Chicago" 
                                    name="city" 
                                    value='Chicago'
                                    onChange={onCityRefChange} 
                                    defaultChecked/>
                                <Form.Check 
                                    type="radio" 
                                    label="New York" 
                                    name="city" 
                                    value='NewYork'
                                    onChange={onCityRefChange} 
                                />
                            </Form.Group>
                        </Form>        
                    </Collapse>
            </Col>
        </Row>);
}