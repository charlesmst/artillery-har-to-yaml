This simple script converts .har files to  [Artillery](https://artillery.io/) yml script. You can use it to simulate a stress test on your website.

# Install
Clone this repository in your local machine

### `git clone https://github.com/charlesmst/artillery-har-to-yaml`
### `cd artillery-har-to-yaml` 

Install python requirements
### `pip install -r requirements.txt`

# Using the script

- Open your target website on chrome
- Press f12 to open chrome dev tools and go to the Network tab
- Refresh your page and navigate through your website
- When you are done, click in Export Har button
- With that .har file run this script. For this example, we will use a .har from Hackernews I generated in my machine
- ### `python convert-har-to-flow.py ./example/new.ycombinator.com.har ./example/hacker-news-example.yml`
- Now you can run artillery on that script
- ### `artillery run example/hacker-news-example.yml`
- You can also customize the generated scenario  phases according to [artillery docs](https://artillery.io/docs/script-reference/).

# Customizing
In `config.py` you can customize the script to ignore certain requests by the url parts(`IGNORE_EXT`). It has some defaults to ignore sockets and static files.

You can also change the `CONVERT_THINK` option. When this option is true, the delays between requests is converted to `think` operations for artillery, adding delays between requests.