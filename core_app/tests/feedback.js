// feedback_spec.js

describe('Feedback Modal', () => {
  beforeEach(() => {
    cy.visit('http://localhost:8080') 
  })

  it('should display modal title', () => {
    cy.get('.modal-title').should('contain', 'Tell us what you think')
  })

  it('should close modal when close button is clicked', () => {
    cy.get('.close-btn').click()
    cy.get('header').should('not.exist')
  })

  it('should display star rating section', () => {
    cy.get('.star-rating').should('exist')
  })

  it('should display category selection dropdown', () => {
    cy.get('.category-select').should('exist')
  })

  it('should display comments section with character limit', () => {
    cy.get('.comment-section').should('exist')
    cy.get('.char-limit').should('contain', 'Maximum 1000 characters.')
  })

  it('should submit feedback when submit button is clicked', () => {
    cy.get('#comments').type('This is a test feedback.')
    cy.get('.submit-btn').click()
    // Add assertions for the submit behavior, e.g., confirmation message or success state
  })
});

