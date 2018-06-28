# A basic crawler

# How to use

- Make sure you have Docker installed on your machine.
- To build the image, type: `docker build -t crawler .`
- You need to specify an output volume for the docker container.  Run the following command, replacing the path with a path to folder on your system: `docker run -it --rm --env URL=https://www.example.com --env OUTPUT_DIR=/usr/src/app/output/ -v /some/output/dir/:/usr/src/app/output/ --name crawl-run crawler`
- Output will appear in the terminal and files will be saved in the location you specified above.

# Bugs

- Crawler is pulling assets from external domains
- File structure borks at certain points
- Invalid URL '': No schema supplied for certain relative images

# The Dream

- All urls shoved in a queue
- Worker pulls from a queue and download
- Worker reports back with info