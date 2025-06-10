import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import styled from 'styled-components';
import { Scale, Home, Search } from 'lucide-react';

const HeaderContainer = styled.header`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const Logo = styled.div`
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: white;
  font-size: 1.5rem;
  font-weight: 700;
`;

const Nav = styled.nav`
  display: flex;
  gap: 2rem;
`;

const NavLink = styled(Link)`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: all 0.2s;
  background: ${props => props.$active ? 'rgba(255, 255, 255, 0.2)' : 'transparent'};

  &:hover {
    background: rgba(255, 255, 255, 0.15);
    transform: translateY(-1px);
  }
`;

function Header() {
  const location = useLocation();

  return (
    <HeaderContainer>
      <Logo>
        <Scale size={32} />
        Legal Research Assistant
      </Logo>
      <Nav>
        <NavLink to="/" $active={location.pathname === '/'}>
          <Home size={20} />
          Home
        </NavLink>
        <NavLink to="/research" $active={location.pathname === '/research'}>
          <Search size={20} />
          Research
        </NavLink>
      </Nav>
    </HeaderContainer>
  );
}

export default Header; 