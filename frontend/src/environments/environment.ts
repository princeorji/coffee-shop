/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-t2it32ng.us.auth0.com', // the auth0 domain prefix
    audience: 'coffeeAPI', // the audience set for the auth0 app
    clientId: '1saAtGau0163ZVVSsaxppz7iZnCl3RoP', // the client id generated for the auth0 app
    callbackURL: 'https://127.0.0.1:5000/login-results', // the base url of the running ionic application. 
  }
};
