import { LinkContainer } from 'react-router-bootstrap'
import { Container, Navbar, Nav } from 'react-bootstrap'

function Header() {
    return (
        <Navbar bg="dark" expand="lg">
            <Container>
                <LinkContainer to="/">
                    <Navbar.Brand>Crypto Screener</Navbar.Brand>
                </LinkContainer>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="me-auto">
                        <LinkContainer to="/">
                            <Nav.Link>Screener</Nav.Link>
                        </LinkContainer>
                        <LinkContainer to="/add">
                            <Nav.Link>Add</Nav.Link>
                        </LinkContainer>
                    </Nav>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    )
}

export default Header;
