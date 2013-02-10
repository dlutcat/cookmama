#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import re
import torndb
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import unicodedata

from tornado.options import define, options

define("port", default=9033, help="run on the given port", type=int)
define("db_host", default="192.168.0.186:34891")
define("db_name", default="cookmama")
define("db_user", default="wjun")
define("db_passwd", default="UmkVpysZnsOh9hucwG22")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/shop/(\d)+", ShopHandler),
            (r"/admin/shop/(\d)+", AdminHandler),
            (r"/j/shop/(\d)+/item/(\d)+", J_MatchShopItemHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            login_url="/auth/login",
            #xsrf_cookies=True,
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            autoescape=None,
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

        # Have one global connection to the blog DB across all handlers
        self.db = torndb.Connection(
            host=options.db_host, database=options.db_name,
            user=options.db_user, password=options.db_passwd)


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        if not user_id: return None
        return self.db.get("SELECT * FROM authors WHERE id = %s", int(user_id))

    def render_json(self, data):
        ret = { 'code': 0 }
        if not isinstance(data, dict):
            ret.update({'data': data})
        else:
            ret = data
        return self.write(ret)


class HomeHandler(BaseHandler):
    def get(self):
        shop_id = self.get_argument('shop', 1)
        shops = self.db.query("SELECT * FROM shop")
        self.render("home.html", shops=shops, tab=1, shop_id=int(shop_id))


class ShopHandler(BaseHandler):
    def get(self, shop_id):
        shop_id = int(shop_id)
        shops = self.db.query("SELECT * FROM shop")
        items = self.db.query('select * from item where id in (select item_id from shop_item where shop_id = %s)' % shop_id)
        self.render("shop.html", shops=shops, tab=1, shop_id=int(shop_id), items=items)


class AdminHandler(BaseHandler):
    def get(self, shop_id):
        shops = self.db.query("SELECT * FROM shop")
        items = self.db.query("SELECT * FROM item")
        shop_items = self.db.query('select item_id from shop_item where shop_id=%s' % shop_id)
        self.render("admin.html", shops=shops, items=items, tab=2,
                    shop_id=int(shop_id), shop_items=[it.item_id for it in shop_items])


class J_MatchShopItemHandler(BaseHandler):
    def post(self, shop_id, item_id):
        match = self.db.get('select * from shop_item where shop_id = %s and item_id = %s' \
                        % (int(shop_id), int(item_id)))
        if match:
            self.db.execute('delete from shop_item where shop_id = %s and item_id = %s' \
                        % (int(shop_id), int(item_id)))
        else:
            self.db.execute('insert into shop_item (shop_id, item_id) values (%s, %s)' \
                        % (int(shop_id), int(item_id)))

        self.write({ 'code': 0, 'msg': 'OK'})


class AuthLoginHandler(BaseHandler, tornado.auth.GoogleMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("openid.mode", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect()

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Google auth failed")
        author = self.db.get("SELECT * FROM authors WHERE email = %s",
                             user["email"])
        if not author:
            # Auto-create first author
            any_author = self.db.get("SELECT * FROM authors LIMIT 1")
            if not any_author:
                author_id = self.db.execute(
                    "INSERT INTO authors (email,name) VALUES (%s,%s)",
                    user["email"], user["name"])
            else:
                self.redirect("/")
                return
        else:
            author_id = author["id"]
        self.set_secure_cookie("user", str(author_id))
        self.redirect(self.get_argument("next", "/"))


class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
