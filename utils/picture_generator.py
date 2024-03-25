from PIL import Image, ImageDraw, ImageFont


class ImageGenerator:
    def __init__(self, adjacency_list, start, end):
        self.adjacency_list = adjacency_list
        self.start = start
        self.end = end
        self.img_size = (660, 660)
        self.node_radius = 40
        self.node_color = 'gray'
        self.font_path = "arial.ttf"
        self.font_size = 40
        self.h_spacing = 95
        self.v_spacing = 120
        self.names = list(self.adjacency_list.keys())
        self.positions = self.calculate_positions()

    def calculate_positions(self):
        central_x, central_y = self.img_size[0] // 2, self.img_size[1] // 2
        positions = [
            (central_x, central_y - 2 * self.v_spacing),  # Line 1
            (central_x - self.h_spacing, central_y - self.v_spacing), (central_x + self.h_spacing, central_y - self.v_spacing),  # Line 2
            (central_x - 2 * self.h_spacing, central_y), (central_x, central_y), (central_x + 2 * self.h_spacing, central_y),
            # Line 3
            (central_x - self.h_spacing, central_y + self.v_spacing), (central_x + self.h_spacing, central_y + self.v_spacing),  # Line 4
            (central_x, central_y + 2 * self.v_spacing)  # Line 5
        ]

        return positions

    def generate_image(self):
        font = ImageFont.truetype(self.font_path, self.font_size)

        img = Image.new('RGB', self.img_size, '#ebebeb')
        draw = ImageDraw.Draw(img)

        for node, connections in self.adjacency_list.items():
            node_index = self.names.index(node)
            node_pos = self.positions[node_index]
            for connection in connections:
                if connection in self.names:  # Check if the connection name exists
                    connection_index = self.names.index(connection)
                    connection_pos = self.positions[connection_index]
                    draw.line([node_pos, connection_pos], fill='black', width=3)


        for i, pos in enumerate(self.positions):
            top_left = (pos[0] - self.node_radius, pos[1] - self.node_radius)
            bottom_right = (pos[0] + self.node_radius, pos[1] + self.node_radius)

            if self.names[i] == self.start or self.names[i] == self.end:
                draw.ellipse([top_left, bottom_right], fill='white', outline=None)

            else:
                draw.ellipse([top_left, bottom_right], fill=self.node_color, outline=None)

            text_size = font.getbbox(self.names[i])
            dx, dy = text_size[2] - text_size[0], text_size[3] - text_size[1]
            text_pos = (pos[0] - dx / 2, pos[1] - dy / 1.4)
            draw.text(text_pos, self.names[i], fill='black', font=font)

        return img